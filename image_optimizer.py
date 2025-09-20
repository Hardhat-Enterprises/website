#!/usr/bin/env python3
"""
Image optimization script for the website
Converts JPG/PNG images to WebP and minifies SVG files to reduce file sizes

Basic usage:
    python image_optimizer.py --convert-webp --input-dir custom_static/assets/img
    python image_optimizer.py --minify-svg --input-dir custom_static/assets/img
    python image_optimizer.py --all --input-dir custom_static/assets/img
"""

import os
import sys
import argparse
import shutil
from pathlib import Path
from PIL import Image
import svglib
from reportlab.graphics import renderPM
from io import BytesIO
import xml.etree.ElementTree as ET
import re

class ImageOptimizer:
    def __init__(self, input_dir, backup=True, quality_photos=80, quality_graphics=90):
        self.input_dir = Path(input_dir)
        self.backup = backup
        self.quality_photos = quality_photos
        self.quality_graphics = quality_graphics
        self.converted_files = []
        self.failed_files = []
        
        # Create backup directory if backup is enabled
        if self.backup:
            self.backup_dir = self.input_dir.parent / f"{self.input_dir.name}_backup"
            self._create_backup()
    
    def _create_backup(self):
        """Makes a backup copy of the original images before processing"""
        if self.backup_dir.exists():
            shutil.rmtree(self.backup_dir)
        shutil.copytree(self.input_dir, self.backup_dir)
        print(f"Backup created at: {self.backup_dir}")
    
    def _is_photo(self, file_path):
        """Checks if the image looks like a photo based on the filename"""
        filename = file_path.name.lower()
        photo_patterns = ['team', 'news', 'profile', 'photo', 'img', 'imgg', 'imggg']
        return any(pattern in filename for pattern in photo_patterns)
    
    def _get_quality(self, file_path):
        """Picks the right quality setting depending on whether it's a photo or graphic"""
        if self._is_photo(file_path):
            return self.quality_photos
        return self.quality_graphics
    
    def convert_to_webp(self, file_path):
        """Converts a JPG or PNG image to WebP format"""
        try:
            # Skip if it's already WebP
            if file_path.suffix.lower() == '.webp':
                print(f"Skipping {file_path.name} (already WebP)")
                return True
            
            # Skip if it's not a JPG or PNG
            if file_path.suffix.lower() not in ['.jpg', '.jpeg', '.png']:
                print(f"Skipping {file_path.name} (unsupported format)")
                return True
            
            # Open the image and convert it
            with Image.open(file_path) as img:
                # Handle images with transparency (WebP doesn't handle RGBA well)
                if img.mode == 'RGBA':
                    # Put it on a white background
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    background.paste(img, mask=img.split()[-1])
                    img = background
                elif img.mode not in ['RGB', 'L']:
                    img = img.convert('RGB')
                
                # Figure out what quality to use
                quality = self._get_quality(file_path)
                
                # Create the new filename
                webp_path = file_path.with_suffix('.webp')
                
                # Save it as WebP
                img.save(webp_path, 'WebP', quality=quality, optimize=True)
                
                # Check how much space we saved
                original_size = file_path.stat().st_size
                webp_size = webp_path.stat().st_size
                reduction = ((original_size - webp_size) / original_size) * 100
                
                print(f"Converted {file_path.name} → {webp_path.name}")
                print(f"   Size: {original_size:,} bytes → {webp_size:,} bytes ({reduction:.1f}% reduction)")
                
                # Delete the original file since we have the WebP version
                file_path.unlink()
                
                self.converted_files.append({
                    'original': str(file_path),
                    'webp': str(webp_path),
                    'original_size': original_size,
                    'webp_size': webp_size,
                    'reduction': reduction
                })
                
                return True
                
        except Exception as e:
            print(f"Failed to convert {file_path.name}: {str(e)}")
            self.failed_files.append(str(file_path))
            return False
    
    def minify_svg(self, file_path):
        """Makes SVG files smaller by removing extra spaces and stuff"""
        try:
            if file_path.suffix.lower() != '.svg':
                return True
            
            # Read the SVG file
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check how big it is now
            original_size = len(content.encode('utf-8'))
            
            # Parse the XML
            root = ET.fromstring(content)
            
            # Clean up extra spaces
            for elem in root.iter():
                if elem.text:
                    elem.text = elem.text.strip()
                if elem.tail:
                    elem.tail = elem.tail.strip()
            
            # Convert it back to text
            minified = ET.tostring(root, encoding='unicode')
            
            # Remove even more extra spaces
            minified = re.sub(r'\s+', ' ', minified)
            minified = re.sub(r'>\s+<', '><', minified)
            
            # Write minified content
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(minified)
            
            # Get new size
            new_size = len(minified.encode('utf-8'))
            reduction = ((original_size - new_size) / original_size) * 100
            
            print(f"Minified {file_path.name}")
            print(f"   Size: {original_size:,} bytes → {new_size:,} bytes ({reduction:.1f}% reduction)")
            
            return True
            
        except Exception as e:
            print(f"Failed to minify {file_path.name}: {str(e)}")
            self.failed_files.append(str(file_path))
            return False
    
    def process_directory(self, convert_webp=False, minify_svg=False):
        """Goes through all images in a directory and processes them"""
        if not self.input_dir.exists():
            print(f"Directory not found: {self.input_dir}")
            return False
        
        print(f"Processing images in: {self.input_dir}")
        print(f"   Convert to WebP: {convert_webp}")
        print(f"   Minify SVG: {minify_svg}")
        print("-" * 50)
        
        # Look for all the image files
        image_extensions = ['.jpg', '.jpeg', '.png', '.svg']
        image_files = []
        
        for ext in image_extensions:
            image_files.extend(self.input_dir.rglob(f'*{ext}'))
        
        print(f"Found {len(image_files)} image files")
        print("-" * 50)
        
        # Go through each file and process it
        for file_path in image_files:
            if convert_webp and file_path.suffix.lower() in ['.jpg', '.jpeg', '.png']:
                self.convert_to_webp(file_path)
            elif minify_svg and file_path.suffix.lower() == '.svg':
                self.minify_svg(file_path)
        
        # Print summary
        self._print_summary()
        
        return True
    
    def _print_summary(self):
        """Shows a summary of what was converted and how much space was saved"""
        print("\n" + "=" * 50)
        print("SUMMARY")
        print("=" * 50)
        
        if self.converted_files:
            total_original_size = sum(f['original_size'] for f in self.converted_files)
            total_webp_size = sum(f['webp_size'] for f in self.converted_files)
            total_reduction = ((total_original_size - total_webp_size) / total_original_size) * 100
            
            print(f"Successfully converted: {len(self.converted_files)} files")
            print(f"Total size reduction: {total_original_size:,} bytes → {total_webp_size:,} bytes")
            print(f"Space saved: {total_reduction:.1f}%")
        
        if self.failed_files:
            print(f"Failed conversions: {len(self.failed_files)} files")
            for failed_file in self.failed_files:
                print(f"   - {failed_file}")
        
        if self.backup:
            print(f"Backup available at: {self.backup_dir}")

def main():
    parser = argparse.ArgumentParser(description='Automated Image Optimization Tool')
    parser.add_argument('--input-dir', '-i', required=True, help='Input directory containing images')
    parser.add_argument('--convert-webp', action='store_true', help='Convert JPG/PNG to WebP')
    parser.add_argument('--minify-svg', action='store_true', help='Minify SVG files')
    parser.add_argument('--all', action='store_true', help='Convert WebP and minify SVG')
    parser.add_argument('--no-backup', action='store_true', help='Skip creating backup')
    parser.add_argument('--quality-photos', type=int, default=80, help='WebP quality for photos (default: 80)')
    parser.add_argument('--quality-graphics', type=int, default=90, help='WebP quality for graphics (default: 90)')
    
    args = parser.parse_args()
    
    # Validate arguments
    if not (args.convert_webp or args.minify_svg or args.all):
        print("You need to specify what to do: --convert-webp, --minify-svg, or --all")
        return 1
    
    if args.all:
        args.convert_webp = True
        args.minify_svg = True
    
    # Create optimizer instance
    optimizer = ImageOptimizer(
        input_dir=args.input_dir,
        backup=not args.no_backup,
        quality_photos=args.quality_photos,
        quality_graphics=args.quality_graphics
    )
    
    # Process images
    success = optimizer.process_directory(
        convert_webp=args.convert_webp,
        minify_svg=args.minify_svg
    )
    
    return 0 if success else 1

if __name__ == '__main__':
    sys.exit(main())
