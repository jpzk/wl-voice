# wl-voice

## Why this tool?

1. ydotool doesn't work reliably 
2. hyprctl dispatch doesn't work reliably

## Use cases

1. Works within any application in Wayland
2. Faster Whisper is optimized for CPU, so works even without fancy GPU

## Stack

1. Rust project
2. Faster whisper
3. Daemon (keeps the STT mode warms) & CLI combo (called via WM hotkey) 

## Functionality 

1. The user runs wl-voiced in the background, could be a systemd service.
2. The user can trigger wl-voice tool via hotkey e.g. MOD+V it will record the voice via microphone and will notify the user back via DBUS that the recording has finished and the transcription is in the clipboard (via wl-copy). 
3. The user can now paste the transcribed text whereever the user pleases, e.g. opencode as a prompt. 

## Output binaries

the output are two binaries:

1. wl-voiced (daemon process that runs faster whispher and waits for commands from the cli tool wl-voice).
2. wl-voice (cli tool that is called by window manager, such as hyprland)

## Installation 

1. Create a Makefile to simplify the build process 
2. In the ideal case this should be part of the linux distribution


