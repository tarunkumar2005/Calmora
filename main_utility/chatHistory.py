import json
import logging
from typing import List, Dict, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

CHAT_HISTORY_ID = 1

def load_chat_history(cursor, table: str, record_id: int = 1) -> List[Dict[str, str]]:
    """
    Loads the chat history from a specified table and record ID.
    
    Args:
        cursor: Database cursor to execute SQL queries.
        table (str): Table name to fetch history from.
        record_id (int): Record ID to identify the chat history entry.

    Returns:
        List[Dict[str, str]]: Parsed chat history as a list of dictionary entries.
    """
    try:
        query = f"SELECT history FROM {table} WHERE id = %s"
        cursor.execute(query, (record_id,))
        result = cursor.fetchone()
        
        if result is None or not result[0]:
            logging.info(f"No chat history found in {table} for record ID {record_id}.")
            return []
        
        return json.loads(result[0])
    
    except Exception as e:
        logging.exception(f"Failed to load chat history from {table}.")
        return []

def add_chat_entry(role: str, content: str, db, cursor, table: str, record_id: int = 1):
    """
    Adds a new chat entry to the specified chat history table.
    
    Args:
        role (str): The role of the participant (e.g., "user", "assistant").
        content (str): The content of the chat message.
        db: Database connection object.
        cursor: Database cursor to execute SQL queries.
        table (str): Table name to update history.
        record_id (int): Record ID to identify the chat history entry.
    """
    try:
        # Load existing history
        query = f"SELECT history FROM {table} WHERE id = %s"
        cursor.execute(query, (record_id,))
        result = cursor.fetchone()
        
        parsed_history = json.loads(result[0]) if result and result[0] else []
        
        # Add new entry to history
        new_entry = {"role": role, "content": content}
        parsed_history.append(new_entry)
        
        # Update history back in the database
        update_query = f"""
            UPDATE {table}
            SET history = %s
            WHERE id = %s;
        """
        cursor.execute(update_query, (json.dumps(parsed_history), record_id))
        db.commit()
        
        logging.info(f"New chat entry added to {table} for record ID {record_id}.")
    
    except Exception as e:
        logging.exception(f"Failed to add chat entry to {table}.")

# Usage examples
def load_main_chat_history(cursor) -> List[Dict[str, str]]:
    return load_chat_history(cursor, "chat_history", CHAT_HISTORY_ID)

def add_main_chat_entry(role: str, content: str, db, cursor):
    add_chat_entry(role, content, db, cursor, "chat_history", CHAT_HISTORY_ID)