# AUR Submission Guide for wl-voice

## Prerequisites

1. **AUR Account**: Create an account at https://aur.archlinux.org/
2. **SSH Key**: Add your SSH public key to your AUR account
3. **Git**: Ensure git is installed and configured

## Files Created

- `PKGBUILD`: Main package build script
- `.SRCINFO`: Package metadata (auto-generated from PKGBUILD)

## Testing Locally

### Option 1: Native Arch Linux
```bash
# Install makepkg if not available
sudo pacman -S base-devel

# Test build (do not install)
makepkg --syncdeps --noconfirm

# Clean up test files
makepkg --clean
```

### Option 2: Docker Testing
Use the provided Docker setup to test on any system:

```bash
# Build and run test environment
docker-compose -f docker-compose.test.yml up --build -d

# Enter the container
docker-compose -f docker-compose.test.yml exec arch-test bash

# Run the test script inside container
./test-aur.sh

# Exit and cleanup
exit
docker-compose -f docker-compose.test.yml down
```

### Option 3: One-liner Docker Test
```bash
# Quick test without docker-compose
docker run --rm -v $(pwd):/workspace archlinux:latest bash -c "
  pacman -Syu --noconfirm base-devel git python python-pip &&
  useradd -m builduser &&
  chown -R builduser:builduser /workspace &&
  cd /workspace &&
  sudo -u builduser makepkg --syncdeps --noconfirm
"
```

## Submitting to AUR

1. **Clone AUR repository**:
   ```bash
   git clone ssh://aur@aur.archlinux.org/wl-voice.git aur-wl-voice
   cd aur-wl-voice
   ```

2. **Copy package files**:
   ```bash
   cp ../PKGBUILD .
   cp ../.SRCINFO .
   ```

3. **Commit and push**:
   ```bash
   git add PKGBUILD .SRCINFO
   git commit -m "Initial import of wl-voice"
   git push origin master
   ```

## Important Notes

- **Update maintainer info**: Edit the maintainer line in `PKGBUILD` with your name and email
- **License**: Add a LICENSE file to your repository if not present
- **Version updates**: When updating, increment `pkgver` or `pkgrel` and regenerate `.SRCINFO`
- **Dependencies**: The package depends on `python`, `portaudio`, and `wl-clipboard`

## Regenerating .SRCINFO

After any changes to `PKGBUILD`:
```bash
makepkg --printsrcinfo > .SRCINFO
```

## Package Description

This AUR package provides:
- `wl-voiced`: Daemon process running Faster Whisper
- `wl-voice`: CLI tool for recording control
- Fully local speech-to-text transcription
- Wayland/Hyprland integration via hotkeys