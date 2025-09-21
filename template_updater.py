#!/usr/bin/env python3
"""
Updates Django templates to use WebP images instead of JPG/PNG
Finds converted WebP files and updates all the template references

Usage:
    python template_updater.py --templates-dir home/templates --static-dir custom_static/assets/img
"""

import os
import sys
import argparse
import re
from pathlib import Path

class TemplateUpdater:
    def __init__(self, templates_dir, static_dir):
        self.templates_dir = Path(templates_dir)
        self.static_dir = Path(static_dir)
        self.updated_files = []
        self.conversion_map = {}
        
        # Build conversion map from existing files
        self._build_conversion_map()
    
    def _build_conversion_map(self):
        """Looks for converted WebP files and maps them to the original JPG/PNG names"""
        print("Scanning for converted images...")
        
        # Find all WebP files
        webp_files = list(self.static_dir.rglob('*.webp'))
        
        for webp_file in webp_files:
            # Get relative path from static_dir
            rel_path = webp_file.relative_to(self.static_dir)
            
            # Check for corresponding JPG/PNG files (they might not exist if already converted)
            # We need to check all possible extensions that could have been converted
            for ext in ['.jpg', '.jpeg', '.png']:
                original_file = webp_file.with_suffix(ext)
                original_rel = str(original_file.relative_to(self.static_dir))
                webp_rel = str(rel_path)
                
                # Store the mapping even if original doesn't exist (for template updates)
                self.conversion_map[original_rel] = webp_rel
                print(f"   Found: {original_rel} → {webp_rel}")
        
        print(f"Found {len(self.conversion_map)} converted images")
    
    def _update_template_file(self, template_file):
        """Updates one template file to use WebP images"""
        try:
            # Convert string to Path if needed
            if isinstance(template_file, str):
                template_file = Path(template_file)
            
            with open(template_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            changes_made = 0
            
            # Go through each converted image and update references
            for original_path, webp_path in self.conversion_map.items():
                # Look for Django static template tags with double quotes
                pattern = r"{%\s*static\s+\"([^\"]*" + re.escape(original_path) + r")\"\s*%}"
                
                def replace_func(match):
                    static_prefix = match.group(1)
                    new_path = static_prefix.replace(original_path, webp_path)
                    return f"{{% static \"{new_path}\" %}}"
                
                new_content = re.sub(pattern, replace_func, content)
                if new_content != content:
                    changes_made += 1
                    content = new_content
                
                # Also check for single quotes
                pattern_single = r"{%\s*static\s+'([^']*" + re.escape(original_path) + r")'\s*%}"
                
                def replace_func_single(match):
                    static_prefix = match.group(1)
                    new_path = static_prefix.replace(original_path, webp_path)
                    return f"{{% static '{new_path}' %}}"
                
                new_content = re.sub(pattern_single, replace_func_single, content)
                if new_content != content:
                    changes_made += 1
                    content = new_content
            
            # Also check for direct src attributes (not as common but worth checking)
            for original_path, webp_path in self.conversion_map.items():
                # Look for src="path/to/image.jpg"
                pattern = r'src="([^"]*' + re.escape(original_path) + r')"'
                replacement = f'src="\\1'.replace(original_path, webp_path) + '"'
                
                new_content = re.sub(pattern, replacement, content)
                if new_content != content:
                    changes_made += 1
                    content = new_content
            
            # Write updated content if changes were made
            if changes_made > 0:
                with open(template_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"Updated {template_file.name}: {changes_made} references")
                self.updated_files.append({
                    'file': str(template_file),
                    'changes': changes_made
                })
                return True
            else:
                print(f"No changes needed in {template_file.name}")
                return False
                
        except Exception as e:
            print(f"Error updating {template_file.name}: {str(e)}")
            return False
    
    def update_templates(self):
        """Goes through all template files and updates them"""
        if not self.templates_dir.exists():
            print(f"❌ Templates directory not found: {self.templates_dir}")
            return False
        
        print(f"Updating templates in: {self.templates_dir}")
        print("-" * 50)
        
        # Find all HTML template files
        template_files = list(self.templates_dir.rglob('*.html'))
        
        if not template_files:
            print("No HTML template files found")
            return False
        
        print(f"Found {len(template_files)} template files")
        print("-" * 50)
        
        # Go through each template file and update it
        updated_count = 0
        for template_file in template_files:
            if self._update_template_file(template_file):
                updated_count += 1
        
        # Print summary
        self._print_summary(updated_count, len(template_files))
        
        return True
    
    def _print_summary(self, updated_count, total_count):
        """Shows what was updated"""
        print("\n" + "=" * 50)
        print("TEMPLATE UPDATE SUMMARY")
        print("=" * 50)
        
        print(f"Updated files: {updated_count}/{total_count}")
        
        if self.updated_files:
            total_changes = sum(f['changes'] for f in self.updated_files)
            print(f"Total references updated: {total_changes}")
            print("\nUpdated files:")
            for file_info in self.updated_files:
                print(f"   - {Path(file_info['file']).name}: {file_info['changes']} changes")
        
        if not self.conversion_map:
            print("No converted images found. Make sure to run image conversion first.")

def main():
    parser = argparse.ArgumentParser(description='Update Django template references for WebP images')
    parser.add_argument('--templates-dir', '-t', required=True, help='Django templates directory')
    parser.add_argument('--static-dir', '-s', required=True, help='Static images directory')
    
    args = parser.parse_args()
    
    # Create updater instance
    updater = TemplateUpdater(
        templates_dir=args.templates_dir,
        static_dir=args.static_dir
    )
    
    # Update templates
    success = updater.update_templates()
    
    return 0 if success else 1

if __name__ == '__main__':
    sys.exit(main())
