import os
import json
import re
import requests
# Assuming models.py is correctly defined and accessible
from models import Facility, IssueType, Priority 

class AIService:
    timeout = 60

    def __init__(self):
        # DeepSeek API configuration - adjust URL to your local setup
        self.deepseek_url = os.environ.get("DEEPSEEK_API_URL", "https://openrouter.ai/api/v1/chat/completions")
        self.deepseek_model = os.environ.get("DEEPSEEK_MODEL", "deepseek/deepseek-chat-v3-0324:free")
        self.deepseek_key = os.environ.get("DEEPSEEK_API_KEY", None)  # Optional, if your API requires a key
        self.facilities_cache = None
        self.load_facilities()
    
    def load_facilities(self):
        """Load facilities from database for context"""
        try:
            # Import app and db within the method to avoid circular imports
            # if AIService is initialized before app/db. This is a common pattern.
            from flask_app import app, db 
            with app.app_context():
                facilities = Facility.query.all()
                self.facilities_cache = [
                    {
                        'name': f.name,
                        'category': f.category,
                        'location': f.location,
                        'description': f.description or '',
                        'is_bookable': f.is_bookable
                    }
                    for f in facilities
                ]
            print(f"Loaded {len(self.facilities_cache)} facilities into cache.")
        except Exception as e:
            print(f"Error loading facilities: {e}")
            self.facilities_cache = []
    
    def _remove_think_tags(self, text: str) -> str:
        """Remove <think>...</think> tags and their content from the model response."""
        return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)

    def _extract_json_from_llm_response(self, raw_content: str) -> dict:
        """
        Attempts to extract and parse a JSON object from a potentially
        markdown-wrapped or raw LLM response string.
        """
        # Remove <think>...</think> tags if present
        cleaned_content = self._remove_think_tags(raw_content)
        # Regex to find JSON within ```json ... ``` or ``` ... ``` code blocks
        json_match = re.search(r"```(?:json)?\s*(.*?)\s*```", cleaned_content, re.DOTALL)
        if json_match:
            json_string = json_match.group(1).strip()
        else:
            json_string = cleaned_content.strip() # Assume it's just the JSON string

        return json.loads(json_string)

    def extract_entities_and_intent(self, user_message: str) -> dict:
        """Extract entities and classify intent from user message using AI"""
        # Ensure facilities_cache is loaded
        if self.facilities_cache is None:
            self.load_facilities()

        try:
            facilities_context = "\n".join([
                f"- {f['name']} ({f['category']}) at {f['location']}"
                for f in self.facilities_cache[:20]  # Limit context size
            ])
            
            prompt = f"""
            Analyze the following user message and extract entities and classify intent.
            
            Available facilities for context:
            {facilities_context}
            
            User message: "{user_message}"
            
            Extract and classify the following:
            1. Intent: One of [search, explore, book, report_issue, check_status, general_info]
            2. Entities:
               - Facility: name of facility mentioned (if any), e.g., "Computer Lab 1", "Library"
               - Location: specific location mentioned (if any), e.g., "Block A", "Level 2"
               - Issue_type: if reporting issue, one of [electrical, hygiene, structural, equipment, security, other]
               - Component: specific component/equipment mentioned (if any), e.g., "projector", "toilet", "AC unit"
            
            Your response must be a valid JSON object. Do not include any text before or after the JSON.
            The JSON structure should be:
            {{
                "intent": "intent_name",
                "entities": {{
                    "facility": "facility_name or null",
                    "location": "location or null",
                    "issue_type": "issue_type or null",
                    "component": "component or null"
                }},
                "confidence": 0.0-1.0
            }}
            """
            
            headers = {"Authorization": f"Bearer {self.deepseek_key}"} if self.deepseek_key else {}

            payload = {
                "model": self.deepseek_model,
                "messages": [
                    {"role": "system", "content": "You are an expert in natural language processing for campus facility management. Always respond ONLY with valid JSON, strictly adhering to the specified schema. Do not include any conversational text or markdown code blocks (e.g., ```json)."},
                    {"role": "user", "content": prompt}
                ],
                "options": {
                    "temperature": 0.3,
                    "num_predict": 300
                },
                "stream": False # Ensure full JSON response at once
            }
            response = requests.post(self.deepseek_url, json=payload, headers=headers, timeout=self.timeout) # Increased timeout
            response.raise_for_status() # Raises HTTPError for bad responses (4xx or 5xx)
            
            result_data = response.json()

            # Correctly access content from Ollama's /api/chat response
            # model_raw_content = result_data.get("message", {}).get("content", "")

            # For OpenRouter.ai: extract content from choices[0]['message']['content']
            choices = result_data.get("choices", [])
            model_raw_content = ""
            if choices and "message" in choices[0]:
                model_raw_content = choices[0]["message"].get("content", "")

            if not model_raw_content:
                raise ValueError("Model returned empty content for entity & intent extraction.")

            result = self._extract_json_from_llm_response(model_raw_content)

            # Basic validation and default values
            extracted_intent = result.get("intent", "general_info")
            extracted_entities = result.get("entities", {})
            extracted_confidence = result.get("confidence", 0.0) # Model might not always provide this

            return {
                "intent": extracted_intent,
                "entities": {
                    "facility": extracted_entities.get("facility", None),
                    "location": extracted_entities.get("location", None),
                    "issue_type": extracted_entities.get("issue_type", None),
                    "component": extracted_entities.get("component", None)
                },
                "confidence": extracted_confidence
            }
            
        except requests.exceptions.Timeout:
            print(f"Error in entity extraction: Request timed out.")
            return {"intent": "general_info", "entities": {}, "confidence": 0.0, "error": "Timeout"}
        except requests.exceptions.RequestException as e:
            print(f"Error communicating with Ollama API for entity extraction: {e}")
            print("Ensure 'ollama serve' is running and the model is available.")
            return {"intent": "general_info", "entities": {}, "confidence": 0.0, "error": f"API error: {e}"}
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON from model response for entity extraction: {e}")
            print(f"Raw model content was: '{model_raw_content}'") # Important for debugging
            return {"intent": "general_info", "entities": {}, "confidence": 0.0, "error": f"JSON parse error: {e}"}
        except ValueError as e: # For "Model returned empty content"
            print(f"Entity extraction error: {e}")
            return {"intent": "general_info", "entities": {}, "confidence": 0.0, "error": f"Model output issue: {e}"}
        except Exception as e:
            print(f"An unexpected error occurred during entity extraction: {e}")
            return {"intent": "general_info", "entities": {}, "confidence": 0.0, "error": f"Unexpected error: {e}"}
    
    def generate_response(self, user_message: str, intent_data: dict, user_context=None) -> str:
        """Generate contextual response based on intent and entities"""
        # Ensure facilities_cache is loaded
        if self.facilities_cache is None:
            self.load_facilities()

        try:
            intent = intent_data.get('intent', 'general_info')
            entities = intent_data.get('entities', {})
            
            # Build context for the LLM
            facilities_context = "\n".join([
                f"- {f['name']} ({f['category']}) at {f['location']}" + 
                (f" - Bookable" if f['is_bookable'] else "")
                for f in self.facilities_cache[:15] # Limit context size
            ])
            
            context_prompt = f"""
            You are the UTM Campus Assistant Chatbot. Your goal is to provide helpful, friendly, and concise information to students regarding campus facilities.

            **Current Date and Time:** {os.getenv("CURRENT_TIME", "Unknown")}
            **Campus Location:** Singapore, Singapore

            **Available Facilities Information:**
            {facilities_context}

            **Current User Input:** "{user_message}"
            **Current Detected Intent:** {intent}
            **Current Extracted Entities:** {entities}
            """
            
            # Build conversation history if user_context is provided (for multi-turn)
            messages = [
                {"role": "system", "content": context_prompt},
            ]
            # If you want to maintain a longer conversation, you'd add past messages here
            if user_context and user_context.get('history'):
                for msg in user_context['history']:
                    messages.append({"role": msg['sender'].replace("bot","assistant"), "content": msg['text']})
            messages.append({"role": "user", "content": user_message})

            # Add specific guidance for response generation based on intent
            response_guidance = """
            Based on the above context, provide a helpful and conversational response.

            - **search/explore intent:** Briefly describe the facility, its location, and primary purpose. If multiple match, list them briefly.
            - **report_issue intent:** Acknowledge the issue, explain the reporting process (e.g., "Please use the 'Report Issue' function..."), and ask for more details if needed (e.g., exact location, severity).
            - **book intent:** Provide booking information for the facility, or guide them to the booking system/process.
            - **check_status intent:** Explain how to check the status of a reported issue (e.g., "You can check the status on your dashboard...").
            - **general_info intent:** Provide general help, list available services, or ask clarifying questions.

            Keep your response concise and directly answer the user's query if possible. If the requested information is not available in your knowledge base, politely state that.
            """
            messages.append({"role": "system", "content": response_guidance}) # Add this as a guiding message

            headers = {"Authorization": f"Bearer {self.deepseek_key}"} if self.deepseek_key else {}

            payload = {
                "model": self.deepseek_model,
                "messages": messages, # Use the built messages array
                "options": {
                    "temperature": 0.7, # Slightly higher temperature for more conversational responses
                    "num_predict": 500  # Allow more tokens for the response
                },
                "stream": False # Get full response at once
            }
            
            response = requests.post(self.deepseek_url, json=payload, headers=headers, timeout=self.timeout) # Increased timeout
            response.raise_for_status() # Raises HTTPError for bad responses (4xx or 5xx)
            
            result_data = response.json()

            # --- CRITICAL FIX: Correctly access the content from Ollama's chat API response ---
            # Ollama's /api/chat returns: {"model": ..., "created_at": ..., "message": {"role": "assistant", "content": "..."}}
            # Access directly via 'message' key.
            # model_raw_content = result_data.get("message", {}).get("content", "").strip()

            # For OpenRouter.ai: extract content from choices[0]['message']['content']
            choices = result_data.get("choices", [])
            model_raw_content = ""
            if choices and "message" in choices[0]:
                model_raw_content = choices[0]["message"].get("content", "")

            if not model_raw_content:
                raise ValueError("Model returned empty response content for generation.")

            # Remove <think>...</think> tags before returning to user
            return self._remove_think_tags(model_raw_content).strip()
            
        except requests.exceptions.Timeout:
            print(f"Error generating response: Request timed out.")
            return self._generate_fallback_response(user_message, intent_data)
        except requests.exceptions.RequestException as e:
            print(f"Error communicating with Ollama API for response generation: {e}")
            print("Please ensure 'ollama serve' is running and the model is available.")
            return self._generate_fallback_response(user_message, intent_data)
        except ValueError as e: # For "Model returned empty content"
            print(f"Response generation error: {e}")
            return self._generate_fallback_response(user_message, intent_data)
        except Exception as e:
            print(f"An unexpected error occurred during response generation: {e}")
            return self._generate_fallback_response(user_message, intent_data)
    
    def _generate_fallback_response(self, user_message: str, intent_data: dict) -> str:
        """Generate rule-based responses when AI generation fails or is unavailable."""
        message_lower = user_message.lower()
        intent = intent_data.get('intent', 'general_info')
        
        # Computer lab queries
        if any(word in message_lower for word in ['computer', 'lab', 'pc', 'workstation']):
            return "🖥️ **Computer Lab 1** is located at **Block A, Level 2**. It has 40 workstations and is available for booking. You can use it for coursework and projects."
        
        # Library queries
        if any(word in message_lower for word in ['library', 'book', 'study', 'reading']):
            return "📚 The **Library** is located at **Block B, Ground Floor**. It's open from 8:00 AM to 10:00 PM and provides study spaces and resources for students."
        
        # Gymnasium queries
        if any(word in message_lower for word in ['gym', 'gymnasium', 'sports', 'exercise', 'fitness']):
            return "🏃 The **Gymnasium** is located at the **Sports Complex**. It's available for booking and hosts various sports activities and fitness programs."
        
        # Hostel queries
        if any(word in message_lower for word in ['hostel', 'accommodation', 'dormitory', 'room']):
            return "🏠 We have accommodation facilities:\n• **Male Hostel Block C** - Hostel Area\n• **Female Hostel Block D** - Hostel Area\n\nBoth provide student accommodation with necessary amenities."
        
        # Cafeteria queries
        if any(word in message_lower for word in ['cafeteria', 'food', 'dining', 'eat', 'meal']):
            return "🍽️ The **Cafeteria** is located at the **Student Center**. It's open from 7:00 AM to 9:00 PM and serves meals throughout the day."
        
        # Location/where queries
        if any(word in message_lower for word in ['where', 'location', 'find']):
            facilities_list = "📍 **UTM Campus Facilities:**\n\n"
            # Ensure facilities_cache is available for fallback
            if self.facilities_cache:
                for facility in self.facilities_cache[:6]:
                    facilities_list += f"• **{facility['name']}** - {facility['location']}\n"
            else:
                facilities_list += "Unable to load facility details at the moment.\n"
            facilities_list += "\nWhat specific facility are you looking for?"
            return facilities_list
        
        # Issue reporting
        if any(word in message_lower for word in ['problem', 'issue', 'broken', 'report', 'complaint']):
            return "🔧 To report a facility issue:\n1. Go to the **Report Issue** page\n2. Describe the problem in detail\n3. Select the issue type and location\n4. Submit your report\n\nYou can track the status of your report from your dashboard."
        
        # Booking queries
        if any(word in message_lower for word in ['book', 'reserve', 'booking']):
            return "📅 **Facility Booking:**\n• Computer Lab 1 - Available for booking\n• Gymnasium - Available for booking\n\nTo book a facility, please contact the facility management or use the booking system if available."
        
        # General help
        return "👋 **UTM Campus Assistant** can help you with:\n\n• 🔍 **Find facilities** - Ask about locations and details\n• 🔧 **Report issues** - Submit facility problems\n• 📅 **Booking info** - Get booking information\n• ℹ️ **General info** - Campus facility questions\n\nWhat can I help you with today?"
    
    def classify_issue_from_description(self, description: str) -> dict:
        """Classify issue type and priority from description"""
        try:
            prompt = f"""
            Analyze this campus facility issue description and classify it according to the provided categories and priority levels.

            Description: "{description}"

            Classification Guidelines:
            1. Issue Type (choose one): electrical, hygiene, structural, equipment, security, other
               - Electrical: power outages, faulty wiring, lighting issues, HVAC electrical problems.
               - Hygiene: cleanliness, sanitation, waste management, pest control.
               - Structural: building damage (walls, roof, floor), leaks, broken fixtures (non-electrical), plumbing issues (burst pipes).
               - Equipment: broken machines (non-HVAC/electrical, e.g., lab equipment, kitchen appliances, projectors), computers, furniture, jammed doors (mechanical).
               - Security: access control issues, broken locks, safety concerns, unauthorized entry, fire alarm malfunctions.
               - Other: miscellaneous issues not fitting clear categories, general inquiries.

            2. Priority (choose one): low, medium, high, urgent
               - Urgent: Immediate safety hazards, critical infrastructure failure (e.g., campus-wide power outage, major flood, active security breach). Requires immediate attention, 24/7 response.
               - High: Major disruptions affecting many users or core operations (e.g., significant water leak in a common area, main server room AC failure, widespread network outage). Requires prompt attention, often within hours.
               - Medium: Moderate issues with some impact (e.g., a broken chair in an office, minor toilet clog, flickering light in one room, non-critical software bug). Can be addressed within a day or two.
               - Low: Minor issues with minimal impact (e.g., loose door handle, request for minor aesthetic repair, light bulb replacement in a less-used area). Can be addressed within a few days or weeks.

            Your response must be a valid JSON object. Do not include any text before or after the JSON.
            The JSON structure should be:
            {{
                "issue_type": "type_category_here",
                "priority": "priority_level_here",
                "reasoning": "brief explanation for the classification"
            }}
            """
            
            headers = {"Authorization": f"Bearer {self.deepseek_key}"} if self.deepseek_key else {}

            payload = {
                "model": self.deepseek_model,
                "messages": [
                    {"role": "system", "content": "You are an expert in campus facility management and issue classification. Always respond ONLY with valid JSON, strictly adhering to the specified schema. Do not include any conversational text or markdown code blocks (e.g., ```json)."},
                    {"role": "user", "content": prompt}
                ],
                "options": {
                    "temperature": 0.3,
                    "num_predict": 300
                },
                "stream": False # Ensure full JSON response at once
            }
            response = requests.post(self.deepseek_url, json=payload, headers=headers, timeout=self.timeout) # Increased timeout
            response.raise_for_status()
            
            result_data = response.json()
            # Correctly access content from Ollama's /api/chat response
            # model_raw_content = result_data.get("message", {}).get("content", "")

            # For OpenRouter.ai: extract content from choices[0]['message']['content']
            choices = result_data.get("choices", [])
            model_raw_content = ""
            if choices and "message" in choices[0]:
                model_raw_content = choices[0]["message"].get("content", "")

            if not model_raw_content:
                raise ValueError("Model returned empty content for issue classification.")

            result = self._extract_json_from_llm_response(model_raw_content)

            # Validate and normalize the parsed result
            return {
                'issue_type': result.get('issue_type', 'other').lower(),
                'priority': result.get('priority', 'medium').lower(),
                'reasoning': result.get('reasoning', 'No specific reasoning provided by model.')
            }
            
        except requests.exceptions.Timeout:
            print(f"Error classifying issue: Request timed out.")
            return {'issue_type': 'other', 'priority': 'medium', 'reasoning': 'Auto-classified: API request timed out.'}
        except requests.exceptions.RequestException as e:
            print(f"Error communicating with Ollama API for issue classification: {e}")
            print("Ensure 'ollama serve' is running and the model is available.")
            return {'issue_type': 'other', 'priority': 'medium', 'reasoning': f'Auto-classified: API communication error ({e})'}
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON from model response for issue classification: {e}")
            print(f"Raw model content was: '{model_raw_content}'") # Important for debugging
            return {'issue_type': 'other', 'priority': 'medium', 'reasoning': f'Auto-classified: Invalid JSON response from model ({e})'}
        except ValueError as e: # For "Model returned empty content"
            print(f"Issue classification error: {e}")
            return {'issue_type': 'other', 'priority': 'medium', 'reasoning': f'Auto-classified: Model output issue ({e})'}
        except Exception as e:
            print(f"An unexpected error occurred during issue classification: {e}")
            return {'issue_type': 'other', 'priority': 'medium', 'reasoning': f'Auto-classified: Unexpected internal error ({e})'}

# Global AI service instance
# This line should ideally be placed in your main app file (e.g., app.py)
# after 'app' and 'db' are defined, or handled via Flask's application factory pattern.
# For now, it remains here, but be mindful of import order in your full application.
ai_service = AIService()