"""
Test package for chatbot_app
"""

import logging
import os

# Configure logging for tests
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(os.path.dirname(__file__), 'test_results.log')),
        logging.StreamHandler()
    ]
)

# Create a logger for test results
test_logger = logging.getLogger('chatbot_tests')
test_logger.setLevel(logging.INFO)

"""
Test suite for the chatbot application.
""" 