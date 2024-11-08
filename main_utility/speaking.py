import logging
import pygame
import tempfile
import requests
import time
import os
from config.config import GET_ELEVENLAB_API_KEY, BRITTENY_HART_VOICE_ID, REVA_HINDI_VOICE_ID

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def speak(text: str, lang: str = 'en', is_stream: bool = False) -> None:
    """
    Sends text to ElevenLabs TTS API and plays the returned audio.
    
    Args:
        text (str): The text to be converted to speech.
        lang (str): Language code, 'en' for English or 'hi' for Hindi.
        is_stream (bool): Whether to stream the audio.
    """
    api_key = GET_ELEVENLAB_API_KEY()
    url = generate_url(lang, is_stream)
    headers = create_headers(api_key)
    data = create_payload(text)

    response = requests.post(url, headers=headers, json=data, stream=True)

    if response.status_code == 200:
        logging.info("Received audio response from API.")
        try:
            temp_file_path = save_audio_to_temp_file(response)
            if validate_audio_file(temp_file_path):
                play_audio(temp_file_path)
            else:
                logging.error("Audio file validation failed.")
        finally:
            cleanup_temp_file(temp_file_path)
    else:
        logging.error("Failed to get audio response: %s %s", response.status_code, response.text)

def generate_url(lang: str, is_stream: bool) -> str:
    """
    Generates the appropriate ElevenLabs API URL based on language and streaming choice.
    """
    voice_id = BRITTENY_HART_VOICE_ID if lang == "en" else REVA_HINDI_VOICE_ID
    url = f'https://api.elevenlabs.io/v1/text-to-speech/{voice_id}'
    if is_stream:
        url += "/stream"
    logging.info(f"Using URL: {url}")
    return url

def create_headers(api_key: str) -> dict:
    """
    Creates headers for the ElevenLabs API request.
    """
    return {
        'xi-api-key': api_key,
        'Content-Type': 'application/json',
        'Accept': 'audio/mpeg'
    }

def create_payload(text: str) -> dict:
    """
    Creates the JSON payload for the ElevenLabs API request.
    """
    return {
        'text': text,
        'model_id': 'eleven_turbo_v2_5',
        'voice_settings': {
            'stability': 0.5,
            'similarity_boost': 0.75
        }
    }

def save_audio_to_temp_file(response) -> str:
    """
    Saves the streamed audio response to a temporary file.
    
    Args:
        response: Response object from the API request.
        
    Returns:
        str: Path to the saved temporary file.
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
        temp_file_path = temp_file.name
        logging.info(f"Saving audio to temp file: {temp_file_path}")
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                temp_file.write(chunk)
    return temp_file_path

def validate_audio_file(file_path: str) -> bool:
    """
    Validates the audio file by checking its size.
    
    Args:
        file_path (str): Path to the audio file.
        
    Returns:
        bool: True if file is valid, False otherwise.
    """
    file_size = os.path.getsize(file_path)
    if file_size < 1024:
        logging.error("Error: MP3 file is too small and likely invalid.")
        return False
    logging.info("Audio file validated successfully.")
    return True

def play_audio(file_path: str) -> None:
    """
    Plays the audio file using pygame.
    
    Args:
        file_path (str): Path to the audio file to play.
    """
    if not pygame.mixer.get_init():
        pygame.mixer.init()
        
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    
    logging.info("Playing audio.")
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)

def cleanup_temp_file(file_path: str) -> None:
    """
    Cleans up the temporary audio file after playback.
    
    Args:
        file_path (str): Path to the temporary file.
    """
    if file_path and os.path.exists(file_path):
        try:
            pygame.mixer.music.unload()  # Ensure Pygame is done with the file
            os.remove(file_path)
            logging.info(f"Temporary file {file_path} deleted.")
        except Exception as e:
            logging.error(f"Failed to delete temporary file {file_path}: {e}")