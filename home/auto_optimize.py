from django.core.management import call_command
from django.conf import settings
from pathlib import Path

def optimize_images_if_needed():
    """Check if images need optimization and run it"""
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
            call_command('optimize_images', '--no-backup')
            print("Image optimization completed!")
            
    except Exception as e:
        print(f"Auto-optimization failed: {e}")
