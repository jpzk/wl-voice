#!/usr/bin/env python3

import argparse
import socket

def main():
    parser = argparse.ArgumentParser(description='wl-voice CLI')
    parser.add_argument('action', choices=['start', 'stop'], help='Action to perform')
    args = parser.parse_args()

    socket_path = '/tmp/wl-voice.sock'
    client_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

    try:
        client_socket.connect(socket_path)
        client_socket.send(args.action.encode('utf-8'))

        response = client_socket.recv(1024).decode('utf-8').strip()
        if response == 'ok':
            if args.action == 'start':
                print("Recording started")
            elif args.action == 'stop':
                print("Recording stopped, transcribing...")
        else:
            print(f"Error: {response}")
    except FileNotFoundError:
        print("Error: wl-voiced daemon is not running")
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        client_socket.close()

if __name__ == '__main__':
    main()