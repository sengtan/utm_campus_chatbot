import os
import json
import re
import requests
from models import Facility, IssueType, Priority

class AIService:
    def __init__(self):
        # DeepSeek API configuration - adjust URL to your local setup
        self.deepseek_url = os.environ.get("DEEPSEEK_API_URL", "http://localhost:11434/v1/chat/completions")
        self.deepseek_model = os.environ.get("DEEPSEEK_MODEL", "deepseek-r1:7b")
        self.facilities_cache = None
        self.load_facilities()
    
    def load_facilities(self):
        """Load facilities from database for context"""
        try:
            from app import app, db
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
        except Exception as e:
            print(f"Error loading facilities: {e}")
            self.facilities_cache = []
    
    def extract_entities_and_intent(self, user_message):
        """Extract entities and classify intent from user message using AI"""
        try:
            facilities_context = "\n".join([
                f"- {f['name']} ({f['category']}) at {f['location']}"
                for f in self.facilities_cache[:20]  # Limit context size
            ])
            
            prompt = f"""
            Analyze the following user message and extract entities and classify intent.
            
            Available facilities:
            {facilities_context}
            
            User message: "{user_message}"
            
            Extract and classify the following:
            1. Intent: One of [search, explore, book, report_issue, check_status, general_info]
            2. Entities:
               - Facility: name of facility mentioned (if any)
               - Location: specific location mentioned (if any)
               - Issue_type: if reporting issue [electrical, hygiene, structural, equipment, security, other]
               - Component: specific component/equipment mentioned (if any)
            
            Respond in JSON format:
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
            
            payload = {
                "model": self.deepseek_model,
                "messages": [
                    {"role": "system", "content": "You are an expert in natural language processing for campus facility management. Always respond with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 500,
                "temperature": 0.3
            }
            
            response = requests.post(self.deepseek_url, json=payload, timeout=30)
            response.raise_for_status()
            
            result_data = response.json()
            content = result_data["choices"][0]["message"]["content"]
            result = json.loads(content)
            return result
            
        except Exception as e:
            print(f"Error in entity extraction: {e}")
            return {
                "intent": "general_info",
                "entities": {},
                "confidence": 0.0
            }
    
    def generate_response(self, user_message, intent_data, user_context=None):
        """Generate contextual response based on intent and entities"""
        try:
            intent = intent_data.get('intent', 'general_info')
            entities = intent_data.get('entities', {})
            
            # Build context
            facilities_context = "\n".join([
                f"- {f['name']} ({f['category']}) at {f['location']}" + 
                (f" - Bookable" if f['is_bookable'] else "")
                for f in self.facilities_cache[:15]
            ])
            
            context = f"""
            You are the UTM Campus Assistant Chatbot helping students with facility-related queries.
            
            Available facilities:
            {facilities_context}
            
            User message: "{user_message}"
            Detected intent: {intent}
            Extracted entities: {entities}
            
            Provide a helpful, friendly response. Keep responses concise but informative.
            
            For different intents:
            - search/explore: Help find facilities or provide information
            - report_issue: Guide them to report the issue and ask for details
            - book: Provide booking information or guide to booking process
            - check_status: Explain how to check issue status
            - general_info: Provide general help and available options
            
            Be conversational and helpful. If you need more information, ask clarifying questions.
            """
            
            payload = {
                "model": self.deepseek_model,
                "messages": [
                    {"role": "system", "content": context},
                    {"role": "user", "content": user_message}
                ],
                "max_tokens": 300,
                "temperature": 0.7
            }
            
            response = requests.post(self.deepseek_url, json=payload, timeout=30)
            response.raise_for_status()
            
            result_data = response.json()
            return result_data["choices"][0]["message"]["content"].strip()
            
        except Exception as e:
            print(f"Error generating response: {e}")
            # Fallback to rule-based responses when OpenAI is unavailable
            return self._generate_fallback_response(user_message, intent_data)
    
    def _generate_fallback_response(self, user_message, intent_data):
        """Generate rule-based responses when OpenAI is unavailable"""
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
            for facility in self.facilities_cache[:6]:
                facilities_list += f"• **{facility['name']}** - {facility['location']}\n"
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
    
    def classify_issue_from_description(self, description):
        """Classify issue type and priority from description"""
        try:
            prompt = f"""
            Analyze this facility issue description and classify it:
            
            Description: "{description}"
            
            Classify:
            1. Issue Type: electrical, hygiene, structural, equipment, security, other
            2. Priority: low, medium, high, urgent
            
            Consider:
            - Electrical: power outages, faulty wiring, lighting issues
            - Hygiene: cleanliness, sanitation, waste management
            - Structural: building damage, leaks, broken fixtures
            - Equipment: broken machines, computers, furniture
            - Security: access issues, safety concerns
            - Other: miscellaneous issues
            
            Priority levels:
            - Urgent: Safety hazards, complete system failures
            - High: Major disruptions, affecting many users
            - Medium: Moderate issues, some impact
            - Low: Minor issues, minimal impact
            
            Respond in JSON:
            {{
                "issue_type": "type",
                "priority": "priority",
                "reasoning": "brief explanation"
            }}
            """
            
            payload = {
                "model": self.deepseek_model,
                "messages": [
                    {"role": "system", "content": "You are an expert in facility management and issue classification. Always respond with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 200,
                "temperature": 0.3
            }
            
            response = requests.post(self.deepseek_url, json=payload, timeout=30)
            response.raise_for_status()
            
            result_data = response.json()
            content = result_data["choices"][0]["message"]["content"]
            result = json.loads(content)
            return {
                'issue_type': result.get('issue_type', 'other'),
                'priority': result.get('priority', 'medium'),
                'reasoning': result.get('reasoning', '')
            }
            
        except Exception as e:
            print(f"Error classifying issue: {e}")
            return {
                'issue_type': 'other',
                'priority': 'medium',
                'reasoning': 'Auto-classified due to processing error'
            }

# Global AI service instance
ai_service = AIService()
