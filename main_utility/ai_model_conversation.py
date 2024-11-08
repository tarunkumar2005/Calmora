import time
import logging
from utils.AI_Response import getting_dynamic_response
from main_utility.language import get_or_select_language
from main_utility.chatHistory import load_chat_history, add_chat_entry
from .speaking import speak
from .listening import listen
from .language import get_user_settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def handle_conversation(db, cursor):
    """
    Manages the conversation flow with the user, including wake-up and sleep commands.
    """
    is_awake = False
    last_active_time = time.time()
    user_language = get_or_select_language(db, cursor)

    while True:
        try:
            # Listen briefly when asleep, checking only for the wake-up command
            if not is_awake:
                user_input = listen(timeout=5, phrase_time_limit=5)
                if 'wake up' in user_input:
                    is_awake = True
                    logging.info("Assistant awakened by user.")
                    speak("Hello! How can I assist you today?", user_language, is_stream=True)
                    last_active_time = time.time()
                continue  # Skip to the next iteration to keep listening for wake-up when asleep

            # Active conversation loop - listens and responds only when awake
            while is_awake:
                user_input = listen(timeout=30, phrase_time_limit=30)

                # Check if the user says "sleep" to deactivate the assistant
                if 'sleep' in user_input:
                    is_awake = False
                    speak("Goodbye!", user_language)
                    logging.info("Assistant put to sleep by user.")
                    break  # Exit the active loop to go back to listening for "wake up"

                # Check for session timeout after 1 hour
                if time.time() - last_active_time > 3600:
                    is_awake = False
                    speak("Session expired. You can wake me up again anytime!", user_language)
                    logging.info("Session expired due to inactivity.")
                    break  # Exit the active loop to go back to listening for "wake up"

                # Process the user's input and generate a response
                if user_input:  # Ensure there is valid input before processing
                    chat_history = load_chat_history(cursor, table='chat_history', record_id=1)
                    response = getting_dynamic_response(user_input, chat_history, user_language, db, cursor)
                    speak(response, user_language)
                    last_active_time = time.time()  # Reset active time after each response

        except Exception as e:
            logging.exception("An error occurred during the conversation handling.")
            speak("Sorry, something went wrong. Please try again.", user_language)