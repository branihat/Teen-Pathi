#!/bin/bash
# Simple Flutter build script for Render

echo "Installing Flutter..."
export FLUTTER_VERSION="3.16.5"
wget -q https://storage.googleapis.com/flutter_infra_release/releases/stable/linux/flutter_linux_${FLUTTER_VERSION}-stable.tar.xz
tar -xf flutter_linux_${FLUTTER_VERSION}-stable.tar.xz
export PATH="$PATH:`pwd`/flutter/bin"

echo "Flutter version:"
flutter --version

echo "Configuring Flutter for web..."
flutter config --enable-web

echo "Building Flutter web app..."
cd frontend
flutter pub get
flutter build web --release

echo "Build complete!"
