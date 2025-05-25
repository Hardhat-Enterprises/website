"""
Django management command to check the search engine connection status.
"""
from django.core.management.base import BaseCommand
from chatbot_app.search_engine import verify_search_connection, get_searchable_models
from datetime import datetime

class Command(BaseCommand):
    help = 'Checks the search engine connection status'

    def handle(self, *args, **options):
        """Handle the command execution."""
        self.stdout.write("\n=== Search Engine Connection Status ===\n")
        
        # Check connection status
        result = verify_search_connection()
        
        # Print status with color coding
        status = result.get('status', 'unknown')
        if status == 'success':
            status_display = self.style.SUCCESS(status)
        elif status == 'partial':
            status_display = self.style.WARNING(status)
        elif status == 'error':
            status_display = self.style.ERROR(status)
        else:
            status_display = status
            
        self.stdout.write(f"Status: {status_display}")
        self.stdout.write(f"Message: {result.get('message', 'No message provided')}")
        
        # Print diagnostics
        if 'diagnostics' in result:
            self.stdout.write("\nDiagnostics:")
            for key, value in result['diagnostics'].items():
                if key == 'timestamp' and isinstance(value, str):
                    try:
                        dt = datetime.fromisoformat(value)
                        value = dt.strftime("%Y-%m-%d %H:%M:%S")
                    except (ValueError, TypeError):
                        pass
                self.stdout.write(f"  {key}: {value}")
                
        # If connection is successful, list available models
        if status == 'success' and result['diagnostics'].get('models_found', 0) > 0:
            models = get_searchable_models()
            self.stdout.write(f"\nAvailable models ({len(models)}):")
            for i, (key, model_class) in enumerate(models.items(), 1):
                self.stdout.write(f"  {i}. {model_class.__name__}") 