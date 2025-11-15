#!/bin/bash

# ---------------------------------------------
# Automated Git Commit & Push Script
# ---------------------------------------------

# Stop the script on any error
set -e

# Customize your commit message (or pass it as an argument)
COMMIT_MSG=${1:-"Auto-commit: update project files"}

# Print header
echo "---------------------------------------------"
echo "Starting Git Auto Push..."
echo "---------------------------------------------"

# Add all files
git add .

# Commit changes
git commit -m "$COMMIT_MSG"

# Pull latest remote changes (avoid conflicts)
git pull origin main --rebase

# Push to GitHub
git push origin main

echo "---------------------------------------------"
echo "Successfully pushed to GitHub!"
echo "---------------------------------------------"