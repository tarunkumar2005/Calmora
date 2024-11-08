import logging
from .speaking import speak
from .listening import listen

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

DEFAULT_LANGUAGE = 'en'

def get_or_select_language(db, cursor) -> str:
    """
    Retrieves the user's preferred language from the database, or prompts for selection if not set.
    
    Args:
        db: Database connection object.
        cursor: Database cursor for executing SQL commands.
        
    Returns:
        str: The selected or stored language code.
    """
    user_language = get_user_settings(cursor)
    if not user_language:
        logging.info("No user language found; initiating language selection.")
        user_language = prompt_language_selection()
        set_user_language(db, cursor, user_language)
    else:
        logging.info(f"User language found: {user_language}")
    return user_language

def get_user_settings(cursor) -> str:
    """
    Retrieves the user's preferred language from the database.
    
    Args:
        cursor: Database cursor for executing SQL commands.
        
    Returns:
        str: Language code if found; None otherwise.
    """
    try:
        cursor.execute("SELECT language FROM user_settings WHERE id = 1")
        result = cursor.fetchone()
        return result[0] if result else None
    except Exception as e:
        logging.error("Error fetching user language: %s", e)
        return None

def set_user_language(db, cursor, language: str) -> None:
    """
    Sets or updates the user's preferred language in the database.
    
    Args:
        db: Database connection object.
        cursor: Database cursor for executing SQL commands.
        language (str): Language code to set for the user.
    """
    try:
        cursor.execute("""
            INSERT INTO user_settings (id, language) VALUES (1, %s)
            ON DUPLICATE KEY UPDATE language = VALUES(language);
        """, (language,))
        db.commit()
        logging.info(f"User language set to: {language}")
    except Exception as e:
        logging.error("Error setting user language: %s", e)

def prompt_language_selection() -> str:
    """
    Prompts the user to select a language by speaking or typing, and confirms selection.
    
    Returns:
        str: The selected language code.
    """
    languages = {
        'english': ('en', "English selected!"),
        'hindi': ('hi', "हिंदी चुनी गई!")
    }

    instructions = {
        'en': "Select your language. For English, say English. For Hindi, say Hindi.",
        'hi': "अपनी भाषा का चयन करें। अंग्रेजी के लिए, अंग्रेजी कहें। हिंदी के लिए, हिंदी कहें।"
    }

    # Speak and print instructions in both languages
    for lang_code, message in instructions.items():
        speak(message, lang_code)
        print(message)

    while True:
        lang_response = listen(timeout=5, phrase_time_limit=5).lower()
        logging.info(f"User response for language selection: {lang_response}")
        
        for lang, (code, message) in languages.items():
            if lang in lang_response:
                logging.info(f"Language selected: {code}")
                speak(message, code)
                return code
        
        speak("Invalid language. Please try again.", DEFAULT_LANGUAGE)
        logging.warning("Invalid language selection attempt.")