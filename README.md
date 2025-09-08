# wl-voice

A voice recording and transcription tool for Hyprland, using Whisper for speech-to-text and copying results to clipboard. It's using Faster Whisper (optimized for CPU) and runs **fully locally**. 

## Installation

1. Ensure you have `uv` installed (Python package manager).
2. Run `make install` to build and install the daemon and CLI tools.
   - This creates a virtual environment, installs dependencies, builds executables with PyInstaller, and copies them to `/usr/local/bin`.
3. To uninstall, run `make uninstall`.

## Usage

1. Start the daemon: `wl-voiced` (run in background or as a service).
2. Use the CLI to control recording:
   - Start recording: `wl-voice start`
   - Stop recording and transcribe: `wl-voice stop`

The transcribed text will be copied to your clipboard and a notification will appear.

## Hyprland Setup

Add the following bindings to your Hyprland config (`~/.config/hypr/hyprland.conf`):

```
# Start recording
bind = SUPER, R, exec, wl-voice start

# Stop recording and transcribe
bind = SUPER, S, exec, wl-voice stop
```

Ensure the daemon is running before using the bindings. You can add `wl-voiced` to your startup applications.

## Starting the Daemon with Hyprland

To automatically start the wl-voiced daemon when Hyprland launches, add the following line to your Hyprland config (`~/.config/hypr/hyprland.conf`):

```
exec-once = wl-voiced
```

This ensures the daemon is running in the background whenever you start Hyprland.


