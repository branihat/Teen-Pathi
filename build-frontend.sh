#!/bin/bash
set -e

echo "🚀 Installing Flutter and building web app..."

# Install Flutter
echo "📦 Installing Flutter..."
git clone https://github.com/flutter/flutter.git -b stable --depth 1 /opt/flutter
export PATH="$PATH:/opt/flutter/bin"

# Pre-download dependencies
echo "⚡ Pre-downloading Flutter dependencies..."
flutter precache --web

# Enable web support
flutter config --enable-web

# Navigate to frontend directory
cd frontend

# Get Flutter version
echo "📋 Flutter version:"
flutter --version

# Get dependencies
echo "📦 Installing Flutter dependencies..."
flutter pub get

# Build for web
echo "🔨 Building Flutter web app..."
flutter build web --release --web-renderer html

echo "✅ Build completed successfully!"
echo "📁 Built files are in: frontend/build/web"
