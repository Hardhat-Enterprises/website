#!/bin/bash

# i18n Automation Script
# This script handles internationalization updates with proper git management

set -e  # Exit on any error

echo "🌍 Starting i18n automation process..."

# Configure git user for automation
git config user.name "i18n-bot"
git config user.email "i18n-bot@hardhat.com"

# Check if we're on the correct branch
current_branch=$(git branch --show-current)
echo "📍 Current branch: $current_branch"

# If not on main, switch to main first
if [ "$current_branch" != "main" ]; then
    echo "🔄 Switching to main branch..."
    git checkout main
fi

# Stash any uncommitted changes
echo "💾 Stashing any uncommitted changes..."
git stash push -m "i18n-automation-stash-$(date +%Y%m%d-%H%M%S)" || true

# Pull latest changes
echo "⬇️ Pulling latest changes..."
git pull origin main

# Check if i18n branch exists, if not create it
if ! git show-ref --verify --quiet refs/heads/chore/i18n-auto-updates; then
    echo "🌿 Creating i18n branch..."
    git checkout -b chore/i18n-auto-updates
else
    echo "🌿 Switching to i18n branch..."
    git checkout chore/i18n-auto-updates
fi

# Pull latest changes from i18n branch
echo "⬇️ Pulling latest i18n changes..."
git pull origin chore/i18n-auto-updates || true

# Here you would run your i18n translation commands
# For example:
# python manage.py makemessages -a
# python manage.py compilemessages

echo "🔄 Running i18n translation commands..."
# Add your actual i18n commands here
# python manage.py makemessages -a
# python manage.py compilemessages

# Check for changes
if git diff --quiet && git diff --cached --quiet; then
    echo "✅ No changes to commit"
else
    echo "📝 Committing i18n changes..."
    git add .
    git commit -m "chore(i18n): auto-translate & normalise & compile [$(date +%Y-%m-%d)]"
    
    echo "⬆️ Pushing changes..."
    git push origin chore/i18n-auto-updates
fi

# Switch back to main
echo "🔄 Switching back to main branch..."
git checkout main

echo "✅ i18n automation completed successfully!"
