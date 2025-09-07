from django.core.management.base import BaseCommand
from django.core.management import call_command
import os
import sys
from pathlib import Path

class Command(BaseCommand):
    help = 'Runs the Django development server and optimizes images if needed'

    def add_arguments(self, parser):
        parser.add_argument(
            '--no-optimization',
            action='store_true',
            help='Skip image optimization and just run the server',
        )
        parser.add_argument(
            '--optimize-only',
            action='store_true',
            help='Only run image optimization, do not start server',
        )
        parser.add_argument(
            '--port',
            type=int,
            default=8000,
            help='Port to run the server on (default: 8000)',
        )

    def handle(self, *args, **options):
        if not options['no_optimization']:
            self.stdout.write('Checking if image optimization is needed...')
            
            # Check if images need optimization
            if self.images_need_optimization():
                self.stdout.write('Images need optimization. Running optimization...')
                try:
                    call_command('optimize_images', '--no-backup')
                    self.stdout.write(
                        self.style.SUCCESS('Image optimization completed!')
                    )
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'Image optimization failed: {e}')
                    )
            else:
                self.stdout.write('Images are already optimized.')
        
        if options['optimize_only']:
            return
        
        # Start the Django development server
        self.stdout.write(f'Starting Django development server on port {options["port"]}...')
        call_command('runserver', f'0.0.0.0:{options["port"]}')

    def images_need_optimization(self):
        """Check if there are any JPG/PNG images that need conversion"""
        static_dir = Path(__file__).parent.parent.parent.parent.parent / "custom_static" / "assets" / "img"
        
        if not static_dir.exists():
            return False
        
        # Look for JPG/PNG files
        for ext in ['.jpg', '.jpeg', '.png']:
            if list(static_dir.rglob(f'*{ext}')):
                return True
        
        return False
