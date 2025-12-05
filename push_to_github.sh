#!/bin/bash
# Quick GitHub Push Script for Emotion Music Generator
# Run this script to push your code to GitHub

echo "╔════════════════════════════════════════════════════════╗"
echo "║     Emotion Music Generator - GitHub Push Helper      ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

# Check if in correct directory
if [ ! -f "requirements.txt" ]; then
    echo "❌ Error: requirements.txt not found!"
    echo "Please run this script from emotion-music-generator2 directory"
    exit 1
fi

echo "✅ Found project files"
echo ""

# Step 1: Configure Git
echo "📝 Step 1: Configure Git User"
echo "Please provide your GitHub information:"
read -p "GitHub Username: " github_user
read -p "Your Full Name: " full_name
read -p "Your Email: " user_email

git config user.name "$full_name"
git config user.email "$user_email"
echo "✅ Git configured"
echo ""

# Step 2: Initialize git if needed
if [ ! -d ".git" ]; then
    echo "📝 Step 2: Initialize Git Repository"
    git init
    echo "✅ Git repository initialized"
    echo ""
fi

# Step 3: Add files
echo "📝 Step 3: Add All Files to Git"
git add .
echo "✅ Files added"
echo ""

# Step 4: Create commit
echo "📝 Step 4: Create Initial Commit"
git commit -m "Initial commit: Emotion Music Generator with complete documentation"
echo "✅ Commit created"
echo ""

# Step 5: Add remote
echo "📝 Step 5: Add GitHub Remote"
echo "Go to https://github.com/new and create a new repository named:"
echo "  emotion-music-generator"
echo "Then copy the repository URL"
echo ""
read -p "Enter your GitHub repository URL: " repo_url

git remote add origin "$repo_url" 2>/dev/null || git remote set-url origin "$repo_url"
echo "✅ Remote repository added"
echo ""

# Step 6: Push
echo "📝 Step 6: Push to GitHub"
git branch -M main
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "╔════════════════════════════════════════════════════════╗"
    echo "║          ✅ Successfully Pushed to GitHub!             ║"
    echo "╚════════════════════════════════════════════════════════╝"
    echo ""
    echo "Your repository is now available at:"
    echo "  $repo_url"
    echo ""
    echo "Next steps:"
    echo "  1. Visit your repository on GitHub"
    echo "  2. Add a project description"
    echo "  3. Add topics: emotion-detection, music-generator"
    echo "  4. Share with your community!"
    echo ""
else
    echo ""
    echo "❌ Error during push. Please check:"
    echo "  1. GitHub repository exists"
    echo "  2. You have push permissions"
    echo "  3. Your GitHub credentials are correct"
    echo ""
    echo "Manual push commands:"
    echo "  git push -u origin main"
    echo ""
fi
