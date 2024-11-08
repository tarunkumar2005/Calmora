import tkinter as tk
from tkinter import scrolledtext
import logging
import threading
import time
from main_utility.listening import listen
from main_utility.speaking import speak
from main_utility.ai_model_conversation import handle_conversation
from main_utility.database import setup_database
from contextlib import closing

# Custom Logging Handler to append logs to Tkinter Text widget
class TkinterLoggingHandler(logging.Handler):
    def __init__(self, text_widget, log_level):
        super().__init__()
        self.text_widget = text_widget
        self.log_level = log_level  # Specify log level to filter

    def emit(self, record):
        # Only display logs of the specified level or higher
        if record.levelno >= self.log_level:
            log_message = self.format(record)  # Format the log message
            self.text_widget.insert("end", log_message + '\n')  # Insert into the text widget
            self.text_widget.yview("end")  # Auto-scroll to the bottom

# Main GUI class
class CalmoraGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        # Set up window
        self.title("Calmora - Real-Time Log Monitor")
        self.geometry("1920x1080")

        # Create ScrolledText widget to display logs
        self.log_text = scrolledtext.ScrolledText(self, width=230, height=50, wrap=tk.WORD)
        self.log_text.grid(row=0, column=0, padx=10, pady=10)

        # Set up logging configuration
        self.setup_logging()

        # Start the process (simulated process)
        self.start_button = tk.Button(self, text="Start Listening", command=self.start_listening)
        self.start_button.grid(row=1, column=0, pady=10)

        self.stop_button = tk.Button(self, text="Stop Listening", command=self.stop_listening)
        self.stop_button.grid(row=2, column=0, pady=10)

        self.is_listening = False

    def setup_logging(self):
        """ Configure logging to display in the GUI. """
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)

        # Create the custom logging handler with the log level filter (INFO level and above)
        handler = TkinterLoggingHandler(self.log_text, logging.INFO)  # Only show INFO and higher logs
        handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))  # Optional format
        self.logger.addHandler(handler)

    def start_listening(self):
        """Start listening and handle conversation."""
        self.is_listening = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

        self.logger.info("Listening started...")
        self.listen_thread = threading.Thread(target=self.listen_and_respond)
        self.listen_thread.start()

    def stop_listening(self):
        """Stop listening and display log messages."""
        self.is_listening = False
        self.logger.info("Listening stopped.")
        self.stop_button.config(state=tk.DISABLED)
        self.start_button.config(state=tk.NORMAL)

    def listen_and_respond(self):
        """Integrate the real listening and speaking logic."""
        db, cursor = self.initialize_database()
        if not db or not cursor:
            self.logger.error("Database initialization failed.")
            return
        
        with closing(db), closing(cursor):
            try:
                # Call handle_conversation without 'user_input' as an argument since it's handled internally
                handle_conversation(db, cursor)

            except Exception as e:
                self.logger.exception("An error occurred during the conversation handling.")
            finally:
                self.logger.info("Conversation loop ended.")

    def initialize_database(self):
        """ Initializes the database. """
        try:
            db, cursor = setup_database()
            if not all([db, cursor]):
                self.logger.error("Failed to connect to the database.")
                return None, None
            self.logger.info("Database connection established.")
            return db, cursor
        except Exception as e:
            self.logger.exception("An error occurred while initializing the database.")
            return None, None

# Main function to initialize the Tkinter GUI and start the application
def main():
    # Initialize your Tkinter GUI
    app = CalmoraGUI()

    # Log the start of the application
    logger = logging.getLogger()
    logger.info("Starting the application...")

    # Run the Tkinter event loop
    app.mainloop()

if __name__ == "__main__":
    main()