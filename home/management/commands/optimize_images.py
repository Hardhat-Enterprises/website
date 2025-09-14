from django.core.management.base import BaseCommand
import os
import sys
import subprocess
from pathlib import Path
from home.models import Profile
from imagekit.utils import get_cache
from django.core.files.base import ContentFile
from PIL import Image
import io


class Command(BaseCommand):
    help = "Optimizes all images by converting JPG/PNG to WebP and minifying SVG files"

    def add_arguments(self, parser):
        parser.add_argument(
            "--no-backup",
            action="store_true",
            help="Skip creating backup before optimization",
        )
        parser.add_argument(
            "--quality-photos",
            type=int,
            default=80,
            help="WebP quality for photos (default: 80)",
        )
        parser.add_argument(
            "--quality-graphics",
            type=int,
            default=90,
            help="WebP quality for graphics (default: 90)",
        )
        parser.add_argument(
            "--convert-original",
            action="store_true",
            help="Overwrite original avatars with WebP",
        )

    def handle(self, *args, **options):
        self.stdout.write("Starting image optimization...")

        # Get the project root directory
        project_root = Path(__file__).parent.parent.parent.parent.parent
        website_dir = project_root / "website"
        static_dir = website_dir / "custom_static" / "assets" / "img"
        templates_dir = website_dir / "home" / "templates"

        # Check if we're in the right directory
        if not static_dir.exists():
            self.stdout.write(
                self.style.ERROR(f"Static directory not found: {static_dir}")
            )
            return

        # Install dependencies first
        self.stdout.write("Installing dependencies...")
        if not self.run_command(
            [sys.executable, "-m", "pip", "install", "-r", "image_requirements.txt"],
            "Installing image processing dependencies",
            website_dir,
        ):
            self.stdout.write(self.style.ERROR("Failed to install dependencies"))
            return

        # Create backup if requested
        if not options["no_backup"]:
            self.stdout.write("Creating backup...")
            if not self.create_git_backup(project_root):
                self.stdout.write(
                    self.style.WARNING("Could not create Git backup (not in Git repo)")
                )

        # Convert images to WebP
        self.stdout.write("Converting images to WebP...")
        if not self.run_command(
            [
                sys.executable,
                "image_optimizer.py",
                "--convert-webp",
                "--input-dir",
                str(static_dir),
                "--quality-photos",
                str(options["quality_photos"]),
                "--quality-graphics",
                str(options["quality_graphics"]),
            ],
            "Converting images to WebP",
            website_dir,
        ):
            self.stdout.write(self.style.ERROR("Failed to convert images to WebP"))
            return

        # Minify SVG files
        self.stdout.write("Minifying SVG files...")
        if not self.run_command(
            [
                sys.executable,
                "image_optimizer.py",
                "--minify-svg",
                "--input-dir",
                str(static_dir),
            ],
            "Minifying SVG files",
            website_dir,
        ):
            self.stdout.write(self.style.ERROR("Failed to minify SVG files"))
            return

        # Update templates
        self.stdout.write("Updating template references...")
        if not self.run_command(
            [
                sys.executable,
                "template_updater.py",
                "--templates-dir",
                str(templates_dir),
                "--static-dir",
                str(static_dir),
            ],
            "Updating template references",
            website_dir,
        ):
            self.stdout.write(self.style.ERROR("Failed to update templates"))
            return

        self.stdout.write(
            self.style.SUCCESS("Image optimization completed successfully!")
        )

        convert_original = options['convert_original']
        profiles = Profile.objects.filter(avatar__isnull=False)
        total = profiles.count()
        self.stdout.write(f"Found {total} profiles with avatars to process.")

        for index, profile in enumerate(profiles, 1):
            try:
                if profile.avatar:
                    profile.avatar_webp_80
                    profile.avatar_webp_70
                    if convert_original:
                        with Image.open(profile.avatar.path) as img:
                            output = io.BytesIO()
                            img.save(output, format='WEBP', quality=80)
                            webp_name = os.path.splitext(profile.avatar.name)[0] + '.webp'
                            profile.avatar.save(webp_name, ContentFile(output.getvalue()), save=True)
                    self.stdout.write(self.style.SUCCESS(
                        f"[{index}/{total}] Processed avatar for {profile.user.email} to WebP"
                    ))
            except Exception as e:
                self.stdout.write(self.style.ERROR(
                    f"[{index}/{total}] Failed to process avatar for {profile.user.email}: {str(e)}"
                ))

        get_cache().clear()
        self.stdout.write(self.style.SUCCESS("Finished processing avatars and cleared cache."))

    def run_command(self, command, description, cwd):
        """Runs a command and handles any errors"""
        try:
            result = subprocess.run(
                command, cwd=cwd, check=True, capture_output=True, text=True
            )
            if result.stdout:
                self.stdout.write(result.stdout)
            if result.stderr:
                self.stdout.write(result.stderr)
            return True
        except subprocess.CalledProcessError as e:
            self.stdout.write(self.style.ERROR(f"Error: {e}"))
            if e.stdout:
                self.stdout.write(f"stdout: {e.stdout}")
            if e.stderr:
                self.stdout.write(f"stderr: {e.stderr}")
            return False

    def create_git_backup(self, project_root):
        """Creates a Git backup of the original files"""
        if not (project_root / ".git").exists():
            return False

        try:
            # Create backup branch
            subprocess.run(
                ["git", "checkout", "-b", "image-optimization-backup"],
                cwd=project_root,
                check=True,
            )

            # Add and commit current state
            subprocess.run(
                ["git", "add", "website/custom_static/assets/img/"],
                cwd=project_root,
                check=True,
            )

            subprocess.run(
                ["git", "commit", "-m", "Backup: Original images before optimization"],
                cwd=project_root,
                check=True,
            )

            # Switch back to main branch
            subprocess.run(["git", "checkout", "main"], cwd=project_root, check=True)

            return True
        except subprocess.CalledProcessError:
            return False
