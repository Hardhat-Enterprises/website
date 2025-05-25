"""
Django management command to test the search function.
"""
import json
import logging
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from chatbot_app.search_engine import perform_search, format_search_results, initialize_search_engine

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Test the search engine functionality"

    def add_arguments(self, parser):
        parser.add_argument('query', type=str, help='The search query to test')
        parser.add_argument('--user', type=str, help='Username to impersonate for search (optional)')
        parser.add_argument('--formatted', action='store_true', help='Show formatted results for display')

    def handle(self, *args, **options):
        """Handle the command execution."""
        query = options['query']
        user = options.get('user')
        show_formatted = options.get('formatted', False)
        
        self.stdout.write(self.style.SUCCESS("\n=== Testing search function ===\n"))
        self.stdout.write(f"Query: \"{query}\"")
        if user:
            self.stdout.write(f"User: {user}")
        
        try:
            # Perform the search
            try:
                results = perform_search(query)
                
                # Display raw results
                self.stdout.write("\nRaw search results:")
                self.stdout.write(json.dumps(results, indent=2, default=str))
                
                # Display search summary
                self.stdout.write(f"\nFound {len(results)} result(s)")
                
                # Get model types
                model_types = set()
                for result in results:
                    if 'model' in result:
                        model_types.add(result['model'])
                
                if model_types:
                    self.stdout.write(f"Results by model type:")
                    for model in model_types:
                        count = sum(1 for r in results if r.get('model') == model)
                        self.stdout.write(f"  - {model}: {count} result(s)")
                
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"\nSearch engine error: {str(e)}"))
                
                # Try to get available models
                try:
                    models_map = initialize_search_engine()
                    self.stdout.write("\nAvailable models:")
                    for name, model in models_map.items():
                        self.stdout.write(f"  - {name}: {model.__name__}")
                except Exception as model_error:
                    self.stdout.write(self.style.ERROR(f"Error getting models: {str(model_error)}"))
            
        except Exception as e:
            raise CommandError(f"Test failed: {e}")
            
        self.stdout.write(self.style.SUCCESS("\nSearch test completed")) 