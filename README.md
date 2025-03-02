# AI Cold Calling Agent (Hinglish)

## Project Overview
The **AI Cold Calling Agent (Hinglish)** is an innovative, AI-driven system designed to conduct personalized and human-like cold calls in Hinglish—a blend of Hindi and English. The agent supports multiple business scenarios:
- **Demo Scheduling:** Schedule product demos for ERP systems.
- **Candidate Interviewing:** Conduct initial screening interviews.
- **Payment/Order Follow-up:** Remind customers about pending payments or order placements.

This project leverages the Gemini generative model for dynamic dialogue generation and integrates speech recognition and text-to-speech capabilities for real-time voice interactions. The graphical user interface (GUI) built with Tkinter provides an intuitive way to manage the conversation and view detailed logs and summaries.

## Project Structure
```
ai_cold_call_agent/
├── data/                     # Optional custom JSON scenario data
├── logs/                     # Conversation logs saved at runtime
├── .env.example              # Environment variable placeholders
├── README.md                 # Project documentation and instructions
├── requirements.txt          # Python package dependencies
├── main.py                   # Main entry point for the application
├── speech_processor.py       # Module for speech recognition and TTS
├── conversation_logger.py    # Module for logging conversations
├── cold_call_agent.py        # AI agent logic for cold calls
└── cold_call_app.py          # Tkinter GUI application
```

## Key Features
- **Conversational AI Integration:**  
  Uses the Gemini generative model to create context-aware responses based on conversation history and scenario-specific prompts.

- **Speech Interaction:**  
  Combines speech recognition (using the SpeechRecognition library) and text-to-speech (via gTTS and pygame) to facilitate real-time voice communication.

- **Graphical User Interface (GUI):**  
  An interactive Tkinter GUI allows users to select the desired scenario, view live conversation logs, and see actionable summaries of the interaction.

- **Conversation Logging:**  
  Each call is logged with detailed turn-by-turn records, timestamps, and conversation metrics, which can be saved for further analysis.

- **Scenario-Specific Customization:**  
  The agent supports loading custom scenario data from JSON files, allowing you to tailor interactions based on customer, job, or invoice information.

## Prerequisites
- Python 3.7 or higher
- Pip package manager

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository_url>
cd ai_cold_call_agent
```

### 2. Install Dependencies
Install the required Python packages using:
```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Copy the provided .env.example file to .env:
```bash
cp .env.example .env
```

Open the .env file and replace YOUR_GEMINI_API_KEY_HERE with your actual Gemini API key.
Ensure other variables are set as needed:
```
SPEECH_RECOGNITION_LANGUAGE=en-IN
TEXT_TO_SPEECH_LANGUAGE=en-IN
TEXT_TO_SPEECH_TLD=co.in
GEMINI_API_KEY=YOUR_GEMINI_API_KEY_HERE
```

### 4. (Optional) Provide Custom Data
If desired, add custom scenario data files in the data/ directory (e.g., demo_data.json, interview_data.json, payment_data.json). Each JSON file should follow a structure similar to:

```json
{
  "customer": {
    "name": "Rahul",
    "company": "XYZ Ltd",
    "interest": "ERP system",
    "email": "rahul@example.com",
    "phone": "+91 98765 43210",
    "location": "Delhi"
  },
  "job": {
    "position": "Data Scientist",
    "skills": "Python, ML, SQL",
    "experience": "2-4 years",
    "salary": "20-25 LPA",
    "location": "Bangalore",
    "work_type": "Remote"
  },
  "invoice": {
    "amount": "5,00,000",
    "days_late": "10",
    "invoice_number": "INV-2023-101",
    "due_date": "31st March 2025",
    "payment_options": "UPI, NEFT, Cheque"
  }
}
```

## Running the Application
Start the application by running:
```bash
python main.py
```

This will launch the Tkinter GUI, where you can select a scenario, start the call, and interact with the agent.

## Demonstration Video
A demonstration video showcasing the agent in action is available here: [LOOM Video Link](#)
(Replace with your actual video URL.)

## Completed Features
- Integration of Gemini generative model for dynamic response generation.
- Real-time speech recognition and text-to-speech functionality.
- Graphical interface with scenario selection, live conversation logging, and actionable summaries.
- Conversation logging with timestamped data for further analysis.
- Customizable scenario data loading from JSON files.

## Partially Implemented / Future Enhancements
- Advanced state management for handling more complex conversations.
- Integration with external calendar or CRM APIs.
- Additional TTS/STT options for improved Hinglish support.
- Sentiment analysis and intent recognition modules.

## Repository Access
Ensure you have granted access to the repository for the following GitHub username:
- rs@imax.co.in

## Final Notes
This project was developed within a 12-hour time frame. Please refer to the code comments for detailed explanations of the implementation. If you have any questions or need further assistance, feel free to reach out.
