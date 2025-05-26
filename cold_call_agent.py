import os
import json
import random
import time
import google.generativeai as genai
from conversation_logger import ConversationLogger
from dotenv import load_dotenv


# Load API keys and configurations from .env
load_dotenv()

# Configuration variables - move API keys to .env
GEMINI_API_KEY = "XXXXXXXXXXXXXXXXXXXXX"
# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

SPEECH_RECOGNITION_LANGUAGE = os.getenv("SPEECH_RECOGNITION_LANGUAGE", "en-IN")
TEXT_TO_SPEECH_LANGUAGE = os.getenv("TEXT_TO_SPEECH_LANGUAGE", "en-IN")
TEXT_TO_SPEECH_TLD = os.getenv("TEXT_TO_SPEECH_TLD", "co.in")


class ColdCallAgent:
    """AI agent for conducting cold calls in Hinglish."""
    
    def __init__(self, scenario, log_callback=None):
        self.scenario = scenario
        self.model = genai.GenerativeModel("gemini-1.5-pro")
        self.conversation_history = []
        self.log_callback = log_callback
        self.logger = ConversationLogger(scenario)
        
        # Load scenario-specific data
        self.load_scenario_data()
        
    def load_scenario_data(self):
        """Load data specific to the selected scenario."""
        # Default data for each scenario
        self.customer_data = {
            "name": "Customer",
            "company": "ABC Corp",
            "interest": "ERP system",
            "email": "customer@example.com",
            "phone": "+91 98765 43210",
            "location": "Mumbai"
        }

        self.job_data = {
            "position": "Software Engineer",
            "skills": "Python, React, Cloud",
            "experience": "3-5 years",
            "salary": "30-35 LPA",
            "location": "Bangalore",
            "work_type": "Hybrid"
        }

        self.invoice_data = {
            "amount": "13,50,000",
            "days_late": "25",
            "invoice_number": "INV-2023-045",
            "due_date": "15th March 2025",
            "payment_options": "UPI, NEFT, Cheque"
        }

        # Load custom data if available
        try:
            scenario_file = f"data/{self.scenario}_data.json"
            if os.path.exists(scenario_file):
                with open(scenario_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                if "customer" in data:
                    if isinstance(data["customer"], list) and data["customer"]:
                        self.customer_data.update(data["customer"][0])
                    else:
                        self.customer_data.update(data["customer"])

                if "job" in data:
                    if isinstance(data["job"], list) and data["job"]:
                        self.job_data.update(data["job"][0])
                    else:
                        self.job_data.update(data["job"])

                if "invoice" in data:
                    if isinstance(data["invoice"], list) and data["invoice"]:
                        self.invoice_data.update(data["invoice"][0])
                    else:
                        self.invoice_data.update(data["invoice"])

                if self.log_callback:
                    self.log_callback(f"✅ Loaded custom data for {self.scenario} scenario")
        except Exception as e:
            if self.log_callback:
                self.log_callback(f"⚠️ Could not load scenario data: {str(e)}")
    
    def generate_response(self, user_input):
        """Generate AI response based on user input with context handling."""
        if self.log_callback:
            self.log_callback("🤖 Thinking...")
        
        # Add user input to conversation history
        if user_input:
            self.conversation_history.append(f"User: {user_input}")
            self.logger.log_turn("user", user_input)
        
        # Get the prompt template based on the scenario
        prompt = self.get_scenario_prompt(user_input)
        
        try:
            # Generate a response using the Gemini model
            response = self.model.generate_content(prompt)
            ai_response = response.text if response.text else "Sorry, I couldn't generate a response."
            
            # Clean the response text
            ai_response = ai_response.replace("AI:", "").replace("Agent:", "").strip()
            
            self.conversation_history.append(f"AI: {ai_response}")
            self.logger.log_turn("ai", ai_response)
            
            return ai_response
            
        except Exception as e:
            error_msg = f"Error generating response: {str(e)}"
            if self.log_callback:
                self.log_callback(f"❌ {error_msg}")
            
            fallback_responses = {
                "demo": "Aapka time dene ke liye dhanyavaad. Kya main aapko ERP demo ke baare mein kuch bata sakta hoon?",
                "interview": "Aapka interview process mein aane ke liye dhanyavaad. Kya aap apne experience ke baare mein bata sakte hain?",
                "payment": "Namaste, main accounts se baat kar raha hoon. Kya aap payment status update kar sakte hain?"
            }
            
            return fallback_responses.get(self.scenario, "Sorry, main aapki help kaise kar sakta hoon?")
    
    def get_scenario_prompt(self, user_input):
        """Get prompt template based on the current scenario."""
        history_text = "\n".join(self.conversation_history[-6:])  # Last 3 turns
        
        scenario_prompts = {
            "demo": f"""
[System Instructions]
You are an ERP sales representative for I-Max India. Your goal is to schedule a demo for the customer.
Your name is Parul Sharma. Speak in Hinglish with a friendly yet professional tone.

[Context]
Customer: {self.customer_data["name"]} from {self.customer_data["company"]}
Interest: {self.customer_data["interest"]}
Location: {self.customer_data["location"]}

[Additional Instructions]
1. Understand the customer's requirements.
2. Explain relevant features briefly.
3. Suggest 2-3 demo time slots.
4. Be polite yet persuasive.
5. Keep responses concise (3-5 sentences).
6. Use natural Hinglish.

[Conversation History]
{history_text}

[Current Input]
Customer: {user_input}

[Your Response in Hinglish]
""",
            "interview": f"""
[System Instructions]
You are Priya Patel, an HR manager conducting a technical screening interview. Speak in natural Hinglish with a professional tone.

[Context]
Position: {self.job_data["position"]}
Required skills: {self.job_data["skills"]}
Experience: {self.job_data["experience"]}
Location: {self.job_data["location"]}
Work type: {self.job_data["work_type"]}

[Additional Instructions]
1. Ask technical questions related to required skills.
2. Follow up on responses for depth.
3. Assess communication and problem-solving skills.
4. Use natural Hinglish.

[Conversation History]
{history_text}

[Current Input]
Candidate: {user_input}

[Your Response in Hinglish]
""",
            "payment": f"""
[System Instructions]
You are Amita Kumari from the accounts department. Your goal is to remind the customer about pending payment.
Speak in Hinglish with a polite but firm tone.

[Context]
Customer: {self.customer_data["name"]} from {self.customer_data["company"]}
Pending Amount: ₹{self.invoice_data["amount"]}
Days Late: {self.invoice_data["days_late"]}
Invoice: {self.invoice_data["invoice_number"]}
Due Date: {self.invoice_data["due_date"]}
Payment Options: {self.invoice_data["payment_options"]}

[Additional Instructions]
1. Politely remind about the pending payment.
2. Mention invoice details and due date.
3. Ask for a commitment on payment.
4. Use natural Hinglish.

[Conversation History]
{history_text}

[Current Input]
Customer: {user_input}

[Your Response in Hinglish]
"""
        }
        return scenario_prompts.get(self.scenario, scenario_prompts["demo"])
    
    def end_conversation(self):
        """End conversation and save the log."""
        metadata = {
            "scenario": self.scenario,
            "customer_data": self.customer_data,
            "turns_count": len(self.conversation_history) // 2
        }
    
        if self.scenario == "demo":
            metadata["job_data"] = self.job_data
        elif self.scenario == "payment":
            metadata["invoice_data"] = self.invoice_data
        elif self.scenario == "interview":
            metadata["candidate_scoring"] = {
                "communication": random.randint(1, 10),
                "technical": random.randint(1, 10),
                "problem_solving": random.randint(1, 10)
            }
    
        log_file = self.logger.save_log(metadata)
    
        if self.log_callback:
            self.log_callback(f"📝 Conversation log saved to {log_file}")
        
        return log_file
