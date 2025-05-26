import os
import time
import threading
import tkinter as tk
from tkinter import ttk, scrolledtext
from speech_processor import SpeechProcessor
from cold_call_agent import ColdCallAgent

class ColdCallApp:
    """GUI Application for the AI Cold Calling Agent (Hinglish)."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("AI Cold Calling Agent (Hinglish)")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        self.scenario_var = tk.StringVar(value="demo")
        self.running = False
        self.agent = None
        self.speech_processor = SpeechProcessor()
        
        self.create_ui()
        
    def create_ui(self):
        """Create the user interface."""
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        title_label = ttk.Label(main_frame, text="AI Cold Calling Agent (Hinglish)", 
                                font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        scenario_frame = ttk.LabelFrame(main_frame, text="Select Scenario", padding="10")
        scenario_frame.pack(fill=tk.X, pady=5)
        
        ttk.Radiobutton(scenario_frame, text="Product Demo Scheduling", 
                        variable=self.scenario_var, value="demo").pack(anchor=tk.W)
        ttk.Radiobutton(scenario_frame, text="Candidate Interviewing", 
                        variable=self.scenario_var, value="interview").pack(anchor=tk.W)
        ttk.Radiobutton(scenario_frame, text="Payment Follow-up", 
                        variable=self.scenario_var, value="payment").pack(anchor=tk.W)
        
        button_frame = ttk.Frame(main_frame, padding="10")
        button_frame.pack(fill=tk.X)
        
        self.start_button = ttk.Button(button_frame, text="Start Call", 
                                       command=self.start_call)
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.end_button = ttk.Button(button_frame, text="End Call", 
                                     command=self.end_call, state=tk.DISABLED)
        self.end_button.pack(side=tk.LEFT, padx=5)
        
        self.speak_button = ttk.Button(button_frame, text="Speak Now", 
                                       command=self.manual_speak, state=tk.DISABLED)
        self.speak_button.pack(side=tk.LEFT, padx=5)
        
        self.status_label = ttk.Label(main_frame, text="Select a scenario and press 'Start Call'", 
                                    font=("Arial", 10), foreground="black")
        self.status_label.pack(pady=5)
        
        log_frame = ttk.LabelFrame(main_frame, text="Conversation Log", padding="10")
        log_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, width=40, height=10)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        self.log_text.config(state=tk.DISABLED)
        
        info_frame = ttk.LabelFrame(main_frame, text="Scenario Information", padding="10")
        info_frame.pack(fill=tk.X, pady=5)
        
        self.info_text = scrolledtext.ScrolledText(info_frame, wrap=tk.WORD, width=40, height=3)
        self.info_text.pack(fill=tk.BOTH)
        self.info_text.config(state=tk.DISABLED)
        
        summary_frame = ttk.LabelFrame(main_frame, text="Actionable Summary", padding="10")
        summary_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        self.summary_text = scrolledtext.ScrolledText(summary_frame, wrap=tk.WORD, width=40, height=3)
        self.summary_text.pack(fill=tk.BOTH, expand=True)
        self.summary_text.config(state=tk.DISABLED)
        
    def log_message(self, message):
        """Add a message to the conversation log."""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
        
    def update_status(self, message, color="black"):
        """Update the status label."""
        self.status_label.config(text=message, foreground=color)
        
    def update_info(self, scenario):
        """Display scenario-specific information."""
        self.info_text.config(state=tk.NORMAL)
        self.info_text.delete(1.0, tk.END)
        
        if scenario == "demo":
            info = (f"Demo Scenario: {self.agent.customer_data['name']} from "
                    f"{self.agent.customer_data['company']} interested in "
                    f"{self.agent.customer_data['interest']}")
        elif scenario == "interview":
            info = (f"Interview for: {self.agent.job_data['position']}\n"
                    f"Skills: {self.agent.job_data['skills']}\n"
                    f"Experience: {self.agent.job_data['experience']}")
        elif scenario == "payment":
            info = (f"Payment due: ₹{self.agent.invoice_data['amount']}\n"
                    f"Days late: {self.agent.invoice_data['days_late']}\n"
                    f"Invoice: {self.agent.invoice_data['invoice_number']}")
        else:
            info = "No information available for this scenario"
            
        self.info_text.insert(tk.END, info)
        self.info_text.config(state=tk.DISABLED)
        
    def start_call(self):
        """Start a new cold call session."""
        scenario = self.scenario_var.get()
        self.running = True
        
        self.start_button.config(state=tk.DISABLED)
        self.end_button.config(state=tk.NORMAL)
        self.speak_button.config(state=tk.NORMAL)
        self.update_status("Call Started! Say something...", "green")
        
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)
        
        self.agent = ColdCallAgent(scenario, self.log_message)
        self.update_info(scenario)
        
        opening_messages = {
            "demo": "Namaskar! Main Parul Sharma bol rahi hoon TechSolutions se. Kya main aapse baat kar sakta hoon ERP system ke demo ke baare mein?",
            "interview": "Namaste! Main Priya Patel, HR manager. Aapka interview schedule kiya hai Software Engineer position ke liye. Kya abhi baat karna convenient hai?",
            "payment": "Namaste! Main Amita Kumari accounts department se baat kar rahi hoon. Aapke payment ke regarding follow up karna tha."
        }
        
        opening = opening_messages.get(scenario, "Namaste! Main Apki kaise help kar sakti hoon?")
        self.log_message(f"AI: {opening}")
        self.speech_processor.speak(opening, self.log_message)
        
        threading.Thread(target=self.conversation_loop, daemon=True).start()
        
    def conversation_loop(self):
        """Continuously listen and process conversation in a separate thread."""
        while self.running:
            user_input = self.speech_processor.recognize_speech(callback=self.log_message)
            
            if not self.running:
                break
                
            if user_input in ["bye", "goodbye", "end call", "stop", "end", "quit", "exit"]:
                self.end_call()
                break
                
            if user_input:
                ai_response = self.agent.generate_response(user_input)
                self.speech_processor.speak(ai_response, self.log_message)
                time.sleep(1)
    
    def manual_speak(self):
        """Manually trigger speech recognition for user input."""
        if self.running and not self.speech_processor.is_listening:
            self.speak_button.config(state=tk.DISABLED)
            
            def speak_thread():
                user_input = self.speech_processor.recognize_speech(callback=self.log_message)
                
                if user_input:
                    if user_input in ["bye", "goodbye", "end call", "stop", "end", "quit", "exit"]:
                        self.root.after(0, self.end_call)
                    else:
                        ai_response = self.agent.generate_response(user_input)
                        self.speech_processor.speak(ai_response, self.log_message)
                
                self.root.after(0, lambda: self.speak_button.config(state=tk.NORMAL))
            
            threading.Thread(target=speak_thread, daemon=True).start()
    
    def end_call(self):
        """Terminate the call and update the UI."""
        if self.running:
            self.running = False
            
            self.start_button.config(state=tk.NORMAL)
            self.end_button.config(state=tk.DISABLED)
            self.speak_button.config(state=tk.DISABLED)
            self.update_status("Call Ended. Thank you!", "red")
            
            if self.agent:
                self.agent.end_conversation()
                
                closing_messages = {
                    "demo": "Thank you for your time! Main jaldi hi aapse demo scheduling ke liye contact karunga. Have a nice day!",
                    "interview": "Interview ke liye dhanyavaad. Humari team aapko result ke baare mein jald hi contact karegi.",
                    "payment": "Baat karne ke liye dhanyavaad. Payment update ke liye wait kar rahe hain. Shubh din!"
                }
                
                closing = closing_messages.get(self.agent.scenario, "Dhanyavaad! Have a nice day!")
                self.log_message(f"AI: {closing}")
                self.speech_processor.speak(closing, self.log_message)
                
                # Update Actionable Summary panel
                summary = self.agent.logger.get_summary()
                summary_text = (
                    f"Total Turns: {summary['total_turns']}\n"
                    f"Duration: {int(summary['duration_seconds'])} seconds\n"
                    f"Key Takeaways: {summary['key_takeaways']}"
                )
                self.summary_text.config(state=tk.NORMAL)
                self.summary_text.delete(1.0, tk.END)
                self.summary_text.insert(tk.END, summary_text)
                self.summary_text.config(state=tk.DISABLED)
