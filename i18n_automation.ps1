# i18n Automation Script (PowerShell)
# This script handles internationalization updates with proper git management

Write-Host "🌍 Starting i18n automation process..." -ForegroundColor Green

# Configure git user for automation
git config user.name "i18n-bot"
git config user.email "i18n-bot@hardhat.com"

# Check current branch
$currentBranch = git branch --show-current
Write-Host "📍 Current branch: $currentBranch" -ForegroundColor Yellow

# If not on main, switch to main first
if ($currentBranch -ne "main") {
    Write-Host "🔄 Switching to main branch..." -ForegroundColor Blue
    git checkout main
}

# Stash any uncommitted changes
Write-Host "💾 Stashing any uncommitted changes..." -ForegroundColor Blue
git stash push -m "i18n-automation-stash-$(Get-Date -Format 'yyyyMMdd-HHmmss')"

# Pull latest changes
Write-Host "⬇️ Pulling latest changes..." -ForegroundColor Blue
git pull origin main

# Check if i18n branch exists, if not create it
$branchExists = git show-ref --verify --quiet refs/heads/chore/i18n-auto-updates
if ($LASTEXITCODE -ne 0) {
    Write-Host "🌿 Creating i18n branch..." -ForegroundColor Green
    git checkout -b chore/i18n-auto-updates
} else {
    Write-Host "🌿 Switching to i18n branch..." -ForegroundColor Green
    git checkout chore/i18n-auto-updates
}

# Pull latest changes from i18n branch
Write-Host "⬇️ Pulling latest i18n changes..." -ForegroundColor Blue
git pull origin chore/i18n-auto-updates

# Here you would run your i18n translation commands
Write-Host "🔄 Running i18n translation commands..." -ForegroundColor Blue
# Add your actual i18n commands here
# python manage.py makemessages -a
# python manage.py compilemessages

# Check for changes
$hasChanges = git diff --quiet; $hasStagedChanges = git diff --cached --quiet
if ($LASTEXITCODE -eq 0 -and $hasStagedChanges) {
    Write-Host "✅ No changes to commit" -ForegroundColor Green
} else {
    Write-Host "📝 Committing i18n changes..." -ForegroundColor Yellow
    git add .
    $date = Get-Date -Format "yyyy-MM-dd"
    git commit -m "chore(i18n): auto-translate & normalise & compile [$date]"
    
    Write-Host "⬆️ Pushing changes..." -ForegroundColor Blue
    git push origin chore/i18n-auto-updates
}

# Switch back to main
Write-Host "🔄 Switching back to main branch..." -ForegroundColor Blue
git checkout main

Write-Host "✅ i18n automation completed successfully!" -ForegroundColor Green


