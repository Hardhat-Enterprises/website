from django.core.management.base import BaseCommand
from django.apps import apps

class Command(BaseCommand):
    help = 'Lists all model classes from the home app'

    def handle(self, *args, **options):
        app_models = apps.get_app_config('home').get_models()
        self.stdout.write("\nFound model classes:")
        for model in app_models:
            self.stdout.write(f"- {model.__name__}") 