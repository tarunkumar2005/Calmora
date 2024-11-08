import logging
import speech_recognition as sr
from main_utility.speaking import speak
from typing import Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def listen(timeout: Optional[int] = None, phrase_time_limit: int = 3, retries: int = 3) -> str:
    """
    Listens to the user's voice input and converts it to text using Google Speech Recognition API.
    
    Args:
        timeout (int, optional): Maximum wait time for a phrase to be started.
        phrase_time_limit (int): Maximum length of a phrase (in seconds).
        retries (int): Number of attempts if recognition fails.
        
    Returns:
        str: Recognized command in lowercase, or an empty string if recognition fails.
    """
    if timeout is not None and timeout <= 0:
        raise ValueError("Timeout must be a positive integer.")
    if phrase_time_limit <= 0:
        raise ValueError("Phrase time limit must be a positive integer.")
    if retries <= 0:
        raise ValueError("Retries must be a positive integer.")
    
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        # Adjust for ambient noise
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        
        for attempt in range(1, retries + 1):
            logging.info(f"Listening attempt {attempt}/{retries}...")
            speak("Listening...", 'en')
            
            try:
                # Capture audio input within specified timeout and phrase limits
                audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
                command = recognizer.recognize_google(audio)
                logging.info(f"Recognized command: {command}")
                print(f"You said: {command}")
                return command.lower()
            
            except sr.UnknownValueError:
                logging.warning("Speech recognition could not understand the audio.")
                speak("Sorry, I didn't catch that. Please repeat.", 'en')
                print("Sorry, I didn't catch that. Please repeat.")
                
            except sr.RequestError:
                logging.error("Google Speech Recognition API is unavailable.")
                speak("Sorry, the speech recognition service is currently unavailable.", 'en')
                print("API unavailable.")
                return ""
                
            except sr.WaitTimeoutError:
                logging.warning("Listening timed out while waiting for speech.")
                speak("Listening timed out. Please try again.", 'en')
                print("Listening timed out.")
        
        logging.error("Maximum retries reached. Unable to recognize speech.")
        speak("Sorry, I couldn't hear you. Please try again.", 'en')
        print("Sorry, I couldn't hear you. Please try again.")
        return ""