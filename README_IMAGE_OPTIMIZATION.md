# Image Optimization Automation

This directory contains scripts for optimizing static images in the Hardhat Enterprises website.

## Quick Start

### 1. Install Dependencies
```bash
cd website
pip install -r image_requirements.txt
```

### 2. Run Optimization

**Automatic optimization (recommended):**
```bash
# Images optimize automatically when you start the server
python manage.py runserver

# Or use the custom server command
python manage.py runserver_with_optimization
```

**Manual optimization:**
```bash
# Complete optimization
python manage.py optimize_images

# Skip backup (faster, but less safe)
python manage.py optimize_images --no-backup

# Using the batch script directly
python batch_optimizer.py
```

**Windows users:**
```bash
# Double-click or run from command prompt
run_with_optimization.bat
```

## Scripts Overview

### `image_optimizer.py`
Main image processing script that:
- Converts JPG/PNG images to WebP format
- Minifies SVG files
- Automatically picks quality settings based on image type
- Creates backups before processing
- Shows detailed progress and statistics

**Usage:**
```bash
# Convert specific directory to WebP
python image_optimizer.py --convert-webp --input-dir custom_static/assets/img/pages/News

# Minify SVG files
python image_optimizer.py --minify-svg --input-dir custom_static/assets/img

# Do both
python image_optimizer.py --all --input-dir custom_static/assets/img
```

### `template_updater.py`
Updates Django template references automatically:
- Finds converted WebP files
- Updates `{% static %}` template tags
- Handles both relative and absolute paths
- Shows detailed change summary

**Usage:**
```bash
python template_updater.py --templates-dir home/templates --static-dir custom_static/assets/img
```

### `batch_optimizer.py`
Does everything automatically:
- Installs dependencies
- Creates Git backups
- Runs image optimization
- Updates templates
- Shows step-by-step progress

**Usage:**
```bash
# Optimize all images
python batch_optimizer.py

# Skip backup for faster processing
python batch_optimizer.py --no-backup
```

### Django Management Commands

**`optimize_images`** - Complete optimization with Django integration:
- Uses Django's management command system
- Integrates with Django's logging
- Shows colored output
- Handles errors gracefully

**Usage:**
```bash
# Complete optimization
python manage.py optimize_images

# Skip backup
python manage.py optimize_images --no-backup

# Custom quality settings
python manage.py optimize_images --quality-photos 85 --quality-graphics 95
```

## Quality Settings

The scripts use smart quality settings:

- **Photos** (team, news, profile images): 80-85% quality
- **Graphics** (logos, icons, diagrams): 90-100% quality
- **SVG files**: Minified by removing whitespace and unnecessary attributes

## Expected Results

### File Size Reductions
- **JPG → WebP**: 25-50% size reduction
- **PNG → WebP**: 20-40% size reduction  
- **SVG minification**: 10-30% size reduction

### Performance Benefits
- Faster page load times
- Reduced bandwidth usage
- Better mobile performance
- Improved Core Web Vitals scores

## 🔧 Manual Usage Examples

### Convert News Images Only
```bash
# 1. Convert images
python image_optimizer.py --convert-webp --input-dir custom_static/assets/img/pages/News --quality-photos 80

# 2. Update templates
python template_updater.py --templates-dir home/templates --static-dir custom_static/assets/img
```

### Convert Team Images
```bash
python image_optimizer.py --convert-webp --input-dir custom_static/assets/img/team --quality-photos 85
```

### Minify All SVG Files
```bash
python image_optimizer.py --minify-svg --input-dir custom_static/assets/img
```

## Safety Features

### Automatic Backups
- Creates Git backup branch before changes
- Preserves original files in `_backup` directory
- Easy rollback if issues occur

### Error Handling
- Continues processing if individual files fail
- Detailed error reporting
- Non-destructive operations

### Validation
- Checks file formats before processing
- Validates directory existence
- Confirms successful conversions

## Verification Checklist

After running optimization:

1. **Check file sizes:**
   ```bash
   # Compare before/after sizes
   ls -la custom_static/assets/img/pages/News/
   ```

2. **Test Django server:**
   ```bash
   python manage.py runserver
   ```

3. **Browser verification:**
   - Open Developer Tools → Network tab
   - Look for `.webp` files loading
   - Check file sizes in Network tab

4. **Visual inspection:**
   - Compare images side-by-side
   - Ensure no quality degradation
   - Verify responsive behavior

## Future Image Processing

For new images added to the project:

1. **Add images to appropriate directories**
2. **Run complete optimization:**
   ```bash
   python manage.py optimize_images
   ```

This will automatically:
- Convert all new JPG/PNG images to WebP
- Minify any new SVG files
- Update all template references
- Create backups before changes

## Troubleshooting

### Common Issues

**"No module named 'PIL'"**
```bash
pip install Pillow
```

**"Permission denied"**
- Ensure you have write permissions to the directories
- Try running as administrator (Windows) or with sudo (Linux/Mac)

**"Template not found"**
- Verify the templates directory path
- Check Django project structure

**"No images found"**
- Verify the static directory path
- Check file extensions (.jpg, .jpeg, .png, .svg)

### Getting Help

1. Check the error messages in the console output
2. Verify file paths and permissions
3. Ensure all dependencies are installed
4. Check that you're running from the correct directory

## Performance Monitoring

After optimization, monitor these metrics:

- **Page Load Speed**: Use browser DevTools
- **File Sizes**: Check Network tab for image sizes
- **Core Web Vitals**: Use Google PageSpeed Insights
- **Bandwidth Usage**: Monitor server logs

## Rollback Process

If you need to revert changes:

```bash
# Restore from Git backup
git checkout image-optimization-backup
git checkout main
git merge image-optimization-backup

# Or restore from file backup
cp -r custom_static/assets/img_backup/* custom_static/assets/img/
```
