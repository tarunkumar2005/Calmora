import mysql.connector
import logging
from mysql.connector import Error
from config.config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME
from typing import Tuple, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def setup_database() -> Tuple[Optional[mysql.connector.MySQLConnection], Optional[mysql.connector.cursor.MySQLCursor]]:
    """
    Sets up the database connection and ensures necessary tables and initial entries are created.
    
    Returns:
        Tuple: Database connection and cursor if successful, (None, None) if there is an error.
    """
    try:
        db = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        
        if db.is_connected():
            logging.info("Connected to MySQL database")
        
        cursor = db.cursor()
        initialize_tables(cursor)
        ensure_initial_entries(cursor, db)
        
        return db, cursor

    except Error as e:
        logging.error("Error connecting to MySQL database: %s", e)
        return None, None

def initialize_tables(cursor: mysql.connector.cursor.MySQLCursor) -> None:
    """
    Ensures that the necessary tables exist in the database.
    
    Args:
        cursor: Database cursor to execute SQL queries.
    """
    try:
        tables = {
            "chat_history": """
                CREATE TABLE IF NOT EXISTS chat_history (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    history JSON
                );
            """,
            "user_settings": """
                CREATE TABLE IF NOT EXISTS user_settings (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    language VARCHAR(2) NOT NULL
                );
            """,
        }
        
        for table_name, create_statement in tables.items():
            cursor.execute(create_statement)
            logging.info(f"Ensured existence of table: {table_name}")
            
    except Error as e:
        logging.error("Error creating tables: %s", e)
        raise

def ensure_initial_entries(cursor: mysql.connector.cursor.MySQLCursor, db: mysql.connector.MySQLConnection) -> None:
    """
    Ensures that each required table has at least one initial entry.
    
    Args:
        cursor: Database cursor to execute SQL queries.
        db: Database connection object to commit transactions.
    """
    try:
        initial_entries = {
            "chat_history": ("SELECT * FROM chat_history", "INSERT INTO chat_history (history) VALUES ('[]')"),
            "user_settings": ("SELECT * FROM user_settings", "INSERT INTO user_settings (language) VALUES ('en')"),
        }

        for table_name, (select_query, insert_query) in initial_entries.items():
            cursor.execute(select_query)
            rows = cursor.fetchall()
            if not rows:
                cursor.execute(insert_query)
                db.commit()
                logging.info(f"Inserted initial entry into {table_name}")
                
    except Error as e:
        logging.error("Error ensuring initial entries: %s", e)
        raise