from django.core.management.base import BaseCommand
from chatbot_app.models import PageContent

class Command(BaseCommand):
    help = 'Initializes default PageContent entries for the chatbot'

    def handle(self, *args, **options):
        self.stdout.write('Creating default PageContent entries...')
        
        try:
            # Call the create_default_entries class method
            PageContent.create_default_entries()
            self.stdout.write(self.style.SUCCESS('Successfully created default PageContent entries!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error creating default entries: {str(e)}')) 