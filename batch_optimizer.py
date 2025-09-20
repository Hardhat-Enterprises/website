#!/usr/bin/env python3
"""
Batch image optimization script
Does everything automatically - converts images, updates templates, creates backups

Usage:
    python batch_optimizer.py
    python batch_optimizer.py --no-backup
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path

class BatchOptimizer:
    def __init__(self, project_root):
        self.project_root = Path(project_root).resolve()
        # If invoked from inside website dir, avoid duplicating path
        if (self.project_root / "website").exists():
            self.website_dir = (self.project_root / "website").resolve()
        else:
            self.website_dir = self.project_root
        self.static_dir = self.website_dir / "custom_static" / "assets" / "img"
        self.templates_dir = self.website_dir / "home" / "templates"
    
    def run_command(self, command, description):
        """Runs a command and handles any errors"""
        print(f"{description}")
        print(f"   Command: {' '.join(command)}")
        print("-" * 50)
        
        try:
            result = subprocess.run(command, cwd=self.website_dir, check=True, 
                                 capture_output=True, text=True)
            print(result.stdout)
            if result.stderr:
                print("Warnings/Info:", result.stderr)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
            print(f"   stdout: {e.stdout}")
            print(f"   stderr: {e.stderr}")
            return False
    
    def install_dependencies(self):
        """Installs the Python packages we need"""
        print("Installing dependencies...")
        return self.run_command([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ], "Installing all project dependencies")
    
    def backup_original_files(self):
        """Makes a Git backup of the original files"""
        print("Creating Git backup...")
        
        # Check if we're in a git repository
        if not (self.project_root / ".git").exists():
            print("Not in a Git repository. Skipping backup.")
            return True
        
        # Create backup branch
        commands = [
            ["git", "checkout", "-b", "image-optimization-backup"],
            ["git", "add", "custom_static/assets/img/"],
            ["git", "commit", "-m", "Backup: Original images before optimization"],
            ["git", "checkout", "main"]
        ]
        
        for cmd in commands:
            if not self.run_command(cmd, f"Running: {' '.join(cmd)}"):
                return False
        
        return True
    
    def optimize_all_images(self):
        """Converts all JPG/PNG images to WebP format"""
        print("Optimizing all images...")
        
        if not self.static_dir.exists():
            print(f"Static directory not found: {self.static_dir}")
            return False
        
        return self.run_command([
            sys.executable, "image_optimizer.py",
            "--convert-webp",
            "--input-dir", str(self.static_dir),
            "--quality-photos", "80",
            "--quality-graphics", "90"
        ], "Converting all images to WebP")
    
    def minify_all_svg(self):
        """Makes all SVG files smaller"""
        print("Minifying SVG files...")
        
        return self.run_command([
            sys.executable, "image_optimizer.py",
            "--minify-svg",
            "--input-dir", str(self.static_dir)
        ], "Minifying all SVG files")
    
    def update_templates(self):
        """Updates Django templates to use the new WebP images"""
        print("Updating template references...")
        
        return self.run_command([
            sys.executable, "template_updater.py",
            "--templates-dir", str(self.templates_dir),
            "--static-dir", str(self.static_dir)
        ], "Updating Django template references")
    
    def run_optimization(self, skip_backup=False):
        """Runs the complete image optimization process"""
        print("Running complete image optimization...")
        print("=" * 60)
        
        steps = [
            ("Installing dependencies", self.install_dependencies),
            ("Creating backup", self.backup_original_files) if not skip_backup else ("Skipping backup", lambda: True),
            ("Converting images to WebP", self.optimize_all_images),
            ("Minifying SVG files", self.minify_all_svg),
            ("Updating templates", self.update_templates)
        ]
        
        for step_name, step_func in steps:
            print(f"\nStep: {step_name}")
            if not step_func():
                print(f"Failed at step: {step_name}")
                return False
            print(f"Completed: {step_name}")
        
        print("\nImage optimization completed successfully!")
        return True

def main():
    parser = argparse.ArgumentParser(description='Batch image optimization tool')
    parser.add_argument('--no-backup', action='store_true', help='Skip creating backup')
    parser.add_argument('--project-root', default='.', help='Project root directory')
    
    args = parser.parse_args()
    
    # Create optimizer instance
    optimizer = BatchOptimizer(args.project_root)
    
    # Run optimization
    success = optimizer.run_optimization(skip_backup=args.no_backup)
    
    return 0 if success else 1

if __name__ == '__main__':
    sys.exit(main())
