from django.core.management.base import BaseCommand
from home.models import CompilerSettings

class Command(BaseCommand):
    help = 'Create default compiler settings'

    def handle(self, *args, **options):
        settings, created = CompilerSettings.objects.get_or_create(
            defaults={
                'max_execution_time': 5,
                'max_memory_limit': 128,
                'max_code_length': 1000,
                'allowed_modules': [],
                'is_active': True
            }
        )
        
        if created:
            self.stdout.write(
                self.style.SUCCESS('Successfully created default compiler settings!')
            )
        else:
            self.stdout.write(
                self.style.WARNING('Compiler settings already exist!')
            )
