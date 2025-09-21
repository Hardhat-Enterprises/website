from django.conf import settings
from pathlib import Path
import os
import sys
import subprocess

def optimize_images_simple():
    """Simple image optimization that runs directly without Django management commands"""
    try:
        # Only run in development mode
        if not settings.DEBUG:
            return
            
        # Check if there are JPG/PNG images that need conversion
        static_dir = Path(settings.BASE_DIR) / "custom_static" / "assets" / "img"
        
        if not static_dir.exists():
            return
        
        # Look for JPG/PNG files
        needs_optimization = False
        for ext in ['.jpg', '.jpeg', '.png']:
            if list(static_dir.rglob(f'*{ext}')):
                needs_optimization = True
                break
        
        if needs_optimization:
            print("Images need optimization. Running optimization...")
            
            # Run the image optimizer directly
            website_dir = Path(settings.BASE_DIR)
            optimizer_script = website_dir / "image_optimizer.py"
            
            if optimizer_script.exists():
                # Convert images to WebP
                subprocess.run([
                    sys.executable, str(optimizer_script),
                    "--convert-webp",
                    "--input-dir", str(static_dir),
                    "--quality-photos", "80",
                    "--quality-graphics", "90"
                ], cwd=website_dir, check=True)
                
                # Minify SVG files
                subprocess.run([
                    sys.executable, str(optimizer_script),
                    "--minify-svg",
                    "--input-dir", str(static_dir)
                ], cwd=website_dir, check=True)
                
                # Update templates
                template_updater_script = website_dir / "template_updater.py"
                templates_dir = website_dir / "home" / "templates"
                
                if template_updater_script.exists():
                    subprocess.run([
                        sys.executable, str(template_updater_script),
                        "--templates-dir", str(templates_dir),
                        "--static-dir", str(static_dir)
                    ], cwd=website_dir, check=True)
                
                print("Image optimization completed!")
            else:
                print("Image optimizer script not found. Skipping optimization.")
            
    except Exception as e:
        print(f"Auto-optimization failed: {e}")
