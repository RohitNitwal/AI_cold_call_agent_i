import os
import time
import json

# Ensure logs directory exists
os.makedirs("logs", exist_ok=True)

class ConversationLogger:
    """Logs conversation data for analysis and improvement."""
    
    def __init__(self, scenario):
        self.scenario = scenario
        self.start_time = time.time()
        self.log_file = f"logs/conversation_{self.scenario}_{int(self.start_time)}.json"
        self.turns = []
    
    def log_turn(self, speaker, text):
        """Log a single conversation turn."""
        self.turns.append({
            "timestamp": time.time(),
            "speaker": speaker,
            "text": text
        })
    
    def save_log(self, metadata=None):
        """Save the conversation log to a file."""
        log_data = {
            "scenario": self.scenario,
            "start_time": self.start_time,
            "end_time": time.time(),
            "duration": time.time() - self.start_time,
            "metadata": metadata or {},
            "turns": self.turns
        }
        
        with open(self.log_file, 'w', encoding='utf-8') as f:
            json.dump(log_data, f, ensure_ascii=False, indent=2)
        
        return self.log_file

    def get_summary(self):
        """Generate a summary of the conversation metrics and key takeaways."""
        summary = {
            "total_turns": len(self.turns),
            "duration_seconds": time.time() - self.start_time,
            "key_takeaways": "Focus on active listening, structured evaluation, and clear communication."
        }
        return summary
