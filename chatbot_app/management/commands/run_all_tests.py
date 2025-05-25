import logging
import subprocess
import sys
import json
from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from django.conf import settings

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Run all chatbot tests to verify functionality"

    def add_arguments(self, parser):
        parser.add_argument('--verbose', action='store_true', help='Show detailed output')
        parser.add_argument('--api-url', type=str, default='http://localhost/api/message/', 
                            help='API URL to test (default: http://localhost/api/message/)')

    def handle(self, *args, **options):
        """Run all tests in sequence"""
        verbose = options.get('verbose', False)
        api_url = options.get('api_url')
        
        self.stdout.write(self.style.SUCCESS("\n===== CHATBOT FULL TEST SUITE =====\n"))
        
        # Test 1: Database connections
        self.stdout.write(self.style.SUCCESS("\n=== 1. Testing Database Connections ===\n"))
        self.run_test_db()
        
        # Test 2: Search with various queries
        self.stdout.write(self.style.SUCCESS("\n=== 2. Testing Search Functionality ===\n"))
        test_queries = [
            "AppAttack",
            "Tell me about AppAttack",
            "Cyber Challenges",
            "Projects",
            "test" # Simple query to test basic functionality
        ]
        
        for query in test_queries:
            self.stdout.write(f"\n>> Testing search query: \"{query}\"\n")
            self.run_search_test(query)
            
        # Test 3: Direct API calls
        self.stdout.write(self.style.SUCCESS("\n=== 3. Testing API Directly ===\n"))
        test_messages = [
            {"message": "Tell me about AppAttack", "sender": "test_user_123"},
            {"message": "What cyber challenges are available?", "sender": "test_user_123"},
            {"message": "What is Deakin Threatmirror?", "sender": "test_user_123"}
        ]
        
        for test_msg in test_messages:
            self.stdout.write(f"\n>> Testing API with message: \"{test_msg['message']}\"\n")
            self.run_api_test(api_url, test_msg, verbose)
            
        self.stdout.write(self.style.SUCCESS("\n===== ALL TESTS COMPLETED =====\n"))
            
    def run_test_db(self):
        """Run the database test command"""
        try:
            call_command('test_db')
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Database test failed: {str(e)}"))
            
    def run_search_test(self, query):
        """Run the search test with a specific query"""
        try:
            call_command('search_test', query)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Search test failed for query '{query}': {str(e)}"))
            
    def run_api_test(self, api_url, message_data, verbose=False):
        """Test the API directly using curl"""
        try:
            # Format the JSON data
            json_data = json.dumps(message_data)
            
            # Build the curl command
            curl_cmd = [
                'curl', '-X', 'POST', 
                '-H', 'Content-Type: application/json',
                '-d', json_data,
                api_url
            ]
            
            if verbose:
                self.stdout.write(f"Running: {' '.join(curl_cmd)}")
            
            # Execute the curl command
            process = subprocess.run(
                curl_cmd,
                capture_output=True,
                text=True
            )
            
            # Process output
            if process.returncode == 0:
                try:
                    # Try to parse as JSON for better formatting
                    response_data = json.loads(process.stdout)
                    self.stdout.write(json.dumps(response_data, indent=2))
                except json.JSONDecodeError:
                    # If not valid JSON, output as is
                    self.stdout.write(process.stdout)
            else:
                self.stdout.write(self.style.ERROR(f"API test failed with status {process.returncode}"))
                self.stdout.write(self.style.ERROR(f"Error: {process.stderr}"))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"API test failed: {str(e)}")) 