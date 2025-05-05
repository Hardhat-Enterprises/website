import logging
import os
from datetime import datetime

# Setup a logger for the test results and write them to a file
def setup_test_logger(filename: str):
    # Create log dir
    log_dir = os.path.join(os.path.dirname(__file__), 'logs')
    os.makedirs(log_dir, exist_ok=True)

    # Instantiate a logger
    logger = logging.getLogger('url_tests')
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        # file handler
        log_file = os.path.join(log_dir, filename)
        file_handler = logging.FileHandler(log_file, mode='w')
        file_handler.setLevel(logging.INFO)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.WARNING)

        # log format
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        return logger

