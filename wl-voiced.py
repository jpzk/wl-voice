#!/usr/bin/env python3

import argparse
import threading
import subprocess
import socket
import os
import sounddevice as sd
import numpy as np
from faster_whisper import WhisperModel

class VoiceDaemon:
    def __init__(self, model_size="base"):
        self.model = WhisperModel(model_size, device="cpu", compute_type="int8")
        self.recording = False
        self.audio_data = []

    def StartRecording(self):
        if not self.recording:
            self.recording = True
            self.audio_data = []
            threading.Thread(target=self._record_audio).start()

    def StopRecording(self):
        if self.recording:
            self.recording = False
            threading.Thread(target=self._transcribe_and_copy).start()

    def _record_audio(self):
        def callback(indata, frames, time, status):
            if self.recording:
                self.audio_data.append(indata.copy())

        with sd.InputStream(callback=callback, channels=1, samplerate=16000):
            while self.recording:
                sd.sleep(100)

    def _transcribe_and_copy(self):
        if self.audio_data:
            audio = np.concatenate(self.audio_data, axis=0).flatten()
            segments, info = self.model.transcribe(audio, language="en")
            text = " ".join([segment.text for segment in segments])
            subprocess.run(['wl-copy'], input=text.encode('utf-8'))
            self._notify_user(text)

    def _notify_user(self, text):
        # Send hyprctl notification
        message = f'Text copied to clipboard: {text[:50]}...'
        subprocess.run(['hyprctl', 'notify', '0', '5000', '0xffffffff', message])

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='wl-voice daemon')
    parser.add_argument('--model', default='base', help='Whisper model size')
    args = parser.parse_args()

    daemon = VoiceDaemon(args.model)

    # Create Unix socket
    socket_path = '/tmp/wl-voice.sock'
    if os.path.exists(socket_path):
        os.unlink(socket_path)

    server_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    server_socket.bind(socket_path)
    server_socket.listen(1)
    print("wl-voiced started")

    try:
        while True:
            client_socket, _ = server_socket.accept()
            try:
                data = client_socket.recv(1024).decode('utf-8').strip()
                if data == 'start':
                    daemon.StartRecording()
                    client_socket.send(b'ok')
                elif data == 'stop':
                    daemon.StopRecording()
                    client_socket.send(b'ok')
                else:
                    client_socket.send(b'error: unknown command')
            except Exception as e:
                client_socket.send(f'error: {str(e)}'.encode('utf-8'))
            finally:
                client_socket.close()
    except KeyboardInterrupt:
        print("Shutting down...")
    finally:
        server_socket.close()
        if os.path.exists(socket_path):
            os.unlink(socket_path)