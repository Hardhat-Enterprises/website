from django.core.management.base import BaseCommand
import os
import sys
import subprocess
from pathlib import Path

class Command(BaseCommand):
    help = 'Runs the complete image optimization process using batch_optimizer.py'

    def add_arguments(self, parser):
        parser.add_argument(
            '--no-backup',
            action='store_true',
            help='Skip creating backup before optimization',
        )

    def handle(self, *args, **options):
        self.stdout.write('Starting image optimization...')
        
        # Get the project root directory
        project_root = Path(__file__).parent.parent.parent.parent.parent
        website_dir = project_root / "website"
        
        # Check if batch_optimizer.py exists
        batch_script = website_dir / "batch_optimizer.py"
        if not batch_script.exists():
            self.stdout.write(
                self.style.ERROR('batch_optimizer.py not found in website directory')
            )
            return
        
        # Build command
        command = [sys.executable, "batch_optimizer.py"]
        if options['no_backup']:
            command.append('--no-backup')
        
        # Run the batch optimizer
        self.stdout.write('Running batch image optimization...')
        try:
            result = subprocess.run(
                command,
                cwd=website_dir,
                check=True,
                capture_output=True,
                text=True
            )
            
            # Display output
            if result.stdout:
                self.stdout.write(result.stdout)
            if result.stderr:
                self.stdout.write(result.stderr)
            
            self.stdout.write(
                self.style.SUCCESS('Image optimization completed successfully!')
            )
            
        except subprocess.CalledProcessError as e:
            self.stdout.write(
                self.style.ERROR(f'Image optimization failed: {e}')
            )
            if e.stdout:
                self.stdout.write(f'stdout: {e.stdout}')
            if e.stderr:
                self.stdout.write(f'stderr: {e.stderr}')
