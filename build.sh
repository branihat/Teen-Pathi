#!/bin/bash
# Build script for Render deployment

echo "Building Flutter web app..."
cd frontend
flutter pub get
flutter build web --release

echo "Build completed successfully!"
echo "Frontend built to: frontend/build/web"
