# Create a file called config.py in the same directory which is config folder and add the following code:

COHERE_API="your_cohere_api_key"
BRITTENY_HART_VOICE_ID = "your_britteny_hart_voice_id"
REVA_HINDI_VOICE_ID = "your_reva_hindi_voice_id"
DB_HOST="your_db_host" # generally localhost
DB_USER="your_db_user" # generally root
DB_PASSWORD="your_db_password"
DB_NAME="mikasha_ai"

elevenlab_api_keys_list = {
  # list of your elevenlab api keys and their status as there is limited number of requests you can make to the api so you might need multiple keys but it is against the terms of service to use multiple keys at the same time so try to use single key at a time
  "your_api_key" : "active",
  "your_api_key" : "inactive",
}

def GET_ELEVENLAB_API_KEY():
    for key, status in elevenlab_api_keys_list.items():
        # Skip any keys that are already marked as "inactive"
        if status == "inactive":
            continue

        url = "https://api.elevenlabs.io/v1/user"
        headers = {
            "xi-api-key": key
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            parsed_response = response.json()

            # Assuming the response contains 'character_count' field
            if parsed_response['subscription']['character_count'] < 9000:
                return key  # Return the first working API key with character count under the limit
            else:
                # Mark the key as "Discarded" if character count exceeds 9000
                elevenlab_api_keys_list[key] = "inactive"
        else:
            # If there's an error, mark this key as "Discarded"
            elevenlab_api_keys_list[key] = "inactive"
            
# Add your own API keys and other sensitive information to this file.