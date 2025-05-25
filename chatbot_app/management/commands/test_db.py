import logging
from django.core.management.base import BaseCommand
from django.db import connections, OperationalError
from chatbot_app.models import ChatSession, ChatMessage
from django.apps import apps

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Test database connections and model access for the chatbot"

    def handle(self, *args, **options):
        # Test general database connection
        self.stdout.write("Testing database connections...")
        
        # Check all database connections
        for conn_name in connections:
            try:
                connection = connections[conn_name]
                connection.cursor()
                self.stdout.write(self.style.SUCCESS(f"✓ Connection '{conn_name}' is working"))
            except OperationalError as e:
                self.stdout.write(self.style.ERROR(f"✗ Connection '{conn_name}' failed: {e}"))
                
        # Test ChatSession model
        self.stdout.write("\nTesting ChatSession model...")
        try:
            session_count = ChatSession.objects.count()
            self.stdout.write(self.style.SUCCESS(f"✓ ChatSession model accessible (found {session_count} records)"))
            
            # Get first session
            if session_count > 0:
                first_session = ChatSession.objects.all().first()
                self.stdout.write(self.style.SUCCESS(f"✓ Sample session ID: {first_session.session_id}"))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"✗ ChatSession model error: {e}"))
            
        # Test ChatMessage model
        self.stdout.write("\nTesting ChatMessage model...")
        try:
            message_count = ChatMessage.objects.count()
            self.stdout.write(self.style.SUCCESS(f"✓ ChatMessage model accessible (found {message_count} records)"))
            
            # Get first message
            if message_count > 0:
                first_message = ChatMessage.objects.all().first()
                self.stdout.write(self.style.SUCCESS(f"✓ Sample message: {first_message.message[:50]}..."))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"✗ ChatMessage model error: {e}"))
            
        # Test related models for search engine
        self.stdout.write("\nTesting models used by search engine...")
        priority_models = [
            'BlogPost',
            'CyberChallenge',
            'Webpage',
            'Project',
        ]
        
        for model_name in priority_models:
            try:
                # Try to get the model
                model = apps.get_model(app_label='home', model_name=model_name)
                count = model.objects.count()
                self.stdout.write(self.style.SUCCESS(f"✓ Model '{model_name}' accessible (found {count} records)"))
                
                # Get schema info for debugging
                fields = [f.name for f in model._meta.fields]
                self.stdout.write(f"  Fields: {', '.join(fields[:5])}{'...' if len(fields) > 5 else ''}")
                
            except LookupError as e:
                self.stdout.write(self.style.WARNING(f"? Model '{model_name}' not found: {e}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"✗ Error accessing model '{model_name}': {e}"))
                
        self.stdout.write("\nDatabase tests completed.") 