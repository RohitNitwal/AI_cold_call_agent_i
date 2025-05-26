import os
import re
import time
import threading
import speech_recognition as sr
from gtts import gTTS
import pygame
from dotenv import load_dotenv
import google.generativeai as genai


# Load API keys and configurations from .env
load_dotenv()

# Configuration variables - move API keys to .env
GEMINI_API_KEY = "XXXXXXXXXXXXXXXXXXXX"
# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

SPEECH_RECOGNITION_LANGUAGE = os.getenv("SPEECH_RECOGNITION_LANGUAGE", "en-IN")
TEXT_TO_SPEECH_LANGUAGE = os.getenv("TEXT_TO_SPEECH_LANGUAGE", "en-IN")
TEXT_TO_SPEECH_TLD = os.getenv("TEXT_TO_SPEECH_TLD", "co.in")


# Initialize pygame mixer for audio playback
pygame.mixer.init()

class SpeechProcessor:
    """Handles speech recognition and synthesis with Hinglish optimization."""
    
    def __init__(self, language=SPEECH_RECOGNITION_LANGUAGE, 
                 tts_language=TEXT_TO_SPEECH_LANGUAGE, 
                 tts_tld=TEXT_TO_SPEECH_TLD):
        self.recognizer = sr.Recognizer()
        self.speech_language = language
        self.tts_language = tts_language
        self.tts_tld = tts_tld
        self.is_listening = False
        self.audio_file = "response.mp3"
    
    def recognize_speech(self, timeout=5, phrase_time_limit=None, callback=None):
        """Capture voice input and convert to text with enhanced error handling."""
        self.is_listening = True
        text = ""
        
        try:
            with sr.Microphone() as source:
                if callback:
                    callback("Listening...")
                
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                self.recognizer.dynamic_energy_threshold = True
                self.recognizer.energy_threshold = 10000
                
                # Listen for audio input
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
                
            if callback:
                callback("Processing speech...")
                
            try:
                text = self.recognizer.recognize_google(audio, language=self.speech_language)
                if callback:
                    callback(f"🗣 User: {text}")
            except sr.UnknownValueError:
                if callback:
                    callback("Could not understand audio")
            except sr.RequestError:
                try:
                    text = self.recognizer.recognize_sphinx(audio)
                    if callback:
                        callback(f"User: {text} (fallback)")
                except Exception as e:
                    if callback:
                        callback("Speech recognition services unavailable")
        except Exception as e:
            if callback:
                callback(f"Error: {str(e)}")
        
        self.is_listening = False
        return text.lower() if text else ""
    
    def speak(self, text, callback=None):
        """Convert text to speech and play it with improved error handling."""
        if not text:
            return
            
        try:
            cleaned_text = re.sub(r"[^\w\s.,!?-]", "", text)
            if callback:
                callback(f"AI: {cleaned_text}")
            
            # Generate speech using gTTS
            tts = gTTS(text=cleaned_text, lang=self.tts_language, slow=False, tld=self.tts_tld)
            tts.save(self.audio_file)
            
            pygame.mixer.music.load(self.audio_file)
            pygame.mixer.music.play()
            
            # Wait for playback to finish
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
            
            pygame.mixer.music.unload()
            
            if os.path.exists(self.audio_file):
                os.remove(self.audio_file)
                
        except Exception as e:
            if callback:
                callback(f"Error in speech synthesis: {str(e)}")
