"""
Django management command to test the format_model_response function.
"""
import json
from django.core.management.base import BaseCommand
from chatbot_app.search_engine import format_model_response, get_searchable_models, search_model
from datetime import datetime

class Command(BaseCommand):
    help = 'Tests the format_model_response function with sample data'

    def add_arguments(self, parser):
        """Add command arguments."""
        parser.add_argument(
            '--model',
            type=str,
            help='Model name to search (e.g., APIModel, Article)',
        )
        parser.add_argument(
            '--term',
            type=str,
            help='Search term to use',
            default='',
        )
        parser.add_argument(
            '--limit',
            type=int,
            help='Number of results to return',
            default=3,
        )

    def handle(self, *args, **options):
        """Handle the command execution."""
        self.stdout.write(self.style.SUCCESS("\n=== Testing format_model_response function ===\n"))
        
        # Get available models
        models = get_searchable_models()
        model_name = options.get('model')
        term = options.get('term', '')
        limit = options.get('limit', 3)
        
        # If no model specified, show available models
        if not model_name:
            self.stdout.write("Available models:")
            for key, model_class in models.items():
                self.stdout.write(f"  - {model_class.__name__}")
            return
            
        # Find the model class
        model_class = None
        for key, cls in models.items():
            if cls.__name__.lower() == model_name.lower():
                model_class = cls
                break
        
        if not model_class:
            self.stdout.write(self.style.ERROR(f"Model {model_name} not found."))
            return
            
        # Search the model
        self.stdout.write(f"Searching {model_class.__name__} for '{term}' (limit: {limit})...")
        results = search_model(model_class, term=term, limit=limit)
        
        self.stdout.write(f"Found {len(results)} results.")
        
        # Format the results
        query_info = {
            'identified_model': model_class.__name__.lower(),
            'search_term': term,
            'timestamp': datetime.now().isoformat()
        }
        
        formatted = format_model_response(results, query_info)
        
        # Print formatted results
        self.stdout.write("\nFormatted response:")
        self.stdout.write(json.dumps(formatted, indent=2, default=str)) 