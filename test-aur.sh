#!/bin/bash

set -e

echo "🔧 Testing AUR package build for wl-voice..."

# Clean any previous build artifacts
echo "📁 Cleaning previous build artifacts..."
rm -rf src/ pkg/ *.pkg.tar.* venv/ dist/ build/ *.spec

# Test PKGBUILD syntax
echo "🔍 Checking PKGBUILD syntax..."
source PKGBUILD
echo "✅ PKGBUILD syntax OK"
echo "   Package: $pkgname"
echo "   Version: $pkgver-$pkgrel" 
echo "   Description: $pkgdesc"

# Install any missing dependencies
echo "📦 Installing build dependencies..."
sudo pacman -S --needed --noconfirm python python-pip portaudio

# Run makepkg to build the package
echo "🔨 Building package with makepkg..."
makepkg --syncdeps --noconfirm --clean

# Check if package was created
PKG_FILE=$(ls *.pkg.tar.* 2>/dev/null | head -n1)
if [ -n "$PKG_FILE" ]; then
    echo "✅ Package built successfully: $PKG_FILE"
    
    # Show package info
    echo "📋 Package information:"
    pacman -Qip "$PKG_FILE"
    
    echo "📁 Package contents:"
    pacman -Qlp "$PKG_FILE"
else
    echo "❌ Package build failed - no .pkg.tar.* file found"
    exit 1
fi

echo "🎉 AUR package test completed successfully!"
echo "📝 Next steps:"
echo "   1. Update maintainer info in PKGBUILD"
echo "   2. Follow AUR-SUBMISSION.md to submit to AUR"