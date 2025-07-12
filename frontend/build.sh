#!/bin/bash
# Frontend build script for Render deployment

echo "🚀 Starting Flutter web build..."

# Install Flutter if not available
if ! command -v flutter &> /dev/null; then
    echo "Installing Flutter..."
    git clone https://github.com/flutter/flutter.git -b stable /opt/flutter
    export PATH="$PATH:/opt/flutter/bin"
fi

# Get Flutter version
flutter --version

# Enable web support
flutter config --enable-web

# Get dependencies
echo "📦 Installing dependencies..."
flutter pub get

# Build for web
echo "🔨 Building Flutter web app..."
flutter build web --release --web-renderer html

echo "✅ Build completed successfully!"
echo "📁 Built files are in: build/web"
