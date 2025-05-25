import logging
import sys
from datetime import datetime

def setup_debug_logging():
    """Configure detailed logging for the chatbot's search process"""
    
    # Create a custom formatter
    class ColoredFormatter(logging.Formatter):
        COLORS = {
            'DEBUG': '\033[36m',    # Cyan
            'INFO': '\033[32m',     # Green
            'WARNING': '\033[33m',   # Yellow
            'ERROR': '\033[31m',    # Red
            'CRITICAL': '\033[41m',  # Red background
            'RESET': '\033[0m'      # Reset
        }

        def format(self, record):
            # Add color to the level name
            level_color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
            record.levelname_colored = f"{level_color}{record.levelname}{self.COLORS['RESET']}"
            
            # Add timestamp
            record.timestamp = datetime.now().strftime('%H:%M:%S.%f')[:-3]
            
            # Format the message
            if record.name == 'chatbot_app.search_engine':
                return f"🔍 [{record.timestamp}] {record.levelname_colored}: {record.getMessage()}"
            elif record.name == 'chatbot_app.textblob_analyzer':
                return f"🧠 [{record.timestamp}] {record.levelname_colored}: {record.getMessage()}"
            elif record.name == 'chatbot_app.views':
                return f"👤 [{record.timestamp}] {record.levelname_colored}: {record.getMessage()}"
            elif record.name == 'chatbot_app.formatter':
                return f"🎨 [{record.timestamp}] {record.levelname_colored}: {record.getMessage()}"
            else:
                return f"[{record.timestamp}] {record.levelname_colored}: {record.getMessage()}"

    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    
    # Set the custom formatter
    formatter = ColoredFormatter()
    console_handler.setFormatter(formatter)
    
    # Configure the logger
    logger = logging.getLogger('chatbot_app')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(console_handler)
    
    # Configure formatter logger specifically
    formatter_logger = logging.getLogger('chatbot_app.formatter')
    formatter_logger.setLevel(logging.DEBUG)
    formatter_logger.addHandler(console_handler)
    
    # Remove any existing handlers to avoid duplicates
    for handler in logger.handlers[:-1]:
        logger.removeHandler(handler)
    
    return logger 