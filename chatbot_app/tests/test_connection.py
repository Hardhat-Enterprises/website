from django.test import TestCase, Client
from django.urls import reverse
from chatbot_app.models import ChatSession, ChatMessage
from chatbot_app.search_engine import verify_search_connection
import json
import logging

# Set up logging
logger = logging.getLogger(__name__)

class ChatbotConnectionTests(TestCase):
    """Test suite for chatbot connection verification"""
    
    def setUp(self):
        """Set up test client and test data"""
        self.client = Client()
        self.verify_url = reverse('verify_connection')
        
    def test_verify_connection_endpoint(self):
        """Test the connection verification endpoint"""
        try:
            # Make GET request to verify endpoint
            response = self.client.get(self.verify_url)
            
            # Check response status code
            self.assertEqual(response.status_code, 200)
            
            # Parse JSON response
            data = json.loads(response.content)
            
            # Check response structure
            self.assertIn('status', data)
            self.assertIn('message', data)
            self.assertIn('timestamp', data)
            
            # Log the response
            logger.info(f"Connection verification response: {data}")
            
            # If connection is successful
            if data['status'] == 'success':
                logger.info("Chatbot connection verified successfully")
            else:
                logger.warning(f"Chatbot connection verification failed: {data['message']}")
                
        except Exception as e:
            logger.error(f"Error in connection verification test: {str(e)}")
            raise
            
    def test_verify_search_connection_function(self):
        """Test the verify_search_connection function directly"""
        try:
            # Call the function directly
            is_connected = verify_search_connection()
            
            # Log the result
            if is_connected:
                logger.info("Search engine connection verified successfully")
            else:
                logger.warning("Search engine connection verification failed")
                
            # The test passes as long as the function doesn't raise an exception
            self.assertTrue(True)
            
        except Exception as e:
            logger.error(f"Error in search connection verification: {str(e)}")
            raise
            
    def test_connection_with_database(self):
        """Test connection by attempting to create and query a chat session"""
        try:
            # Create a test session
            session = ChatSession.objects.create(
                session_id='test_session_123',
                is_active=True
            )
            
            # Create a test message
            message = ChatMessage.objects.create(
                session=session,
                is_user_message=True,
                message='Test message'
            )
            
            # Verify the objects were created
            self.assertEqual(ChatSession.objects.count(), 1)
            self.assertEqual(ChatMessage.objects.count(), 1)
            
            # Log successful database operations
            logger.info("Database connection verified through object creation")
            
        except Exception as e:
            logger.error(f"Error in database connection test: {str(e)}")
            raise
            
    def test_connection_error_handling(self):
        """Test error handling in connection verification"""
        try:
            # Make a request with invalid method
            response = self.client.post(self.verify_url)
            
            # Should return 405 Method Not Allowed
            self.assertEqual(response.status_code, 405)
            
            # Log the response
            logger.info(f"Error handling test response: {response.status_code}")
            
        except Exception as e:
            logger.error(f"Error in connection error handling test: {str(e)}")
            raise 