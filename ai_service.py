import os
import json
import re
from openai import OpenAI
from models import Facility, IssueType, Priority

# the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
# do not change this unless explicitly requested by the user
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "default_key")
openai_client = OpenAI(api_key=OPENAI_API_KEY)

class AIService:
    def __init__(self):
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
            
            response = openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are an expert in natural language processing for campus facility management."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                max_tokens=500
            )
            
            result = json.loads(response.choices[0].message.content)
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
            
            response = openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": context},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=300
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Error generating response: {e}")
            return "I'm sorry, I'm having trouble processing your request right now. Please try again or contact support for assistance."
    
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
            
            response = openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are an expert in facility management and issue classification."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                max_tokens=200
            )
            
            result = json.loads(response.choices[0].message.content)
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
