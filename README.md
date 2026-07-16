# PineTime Heartrate Server
A program to find a PineTime watch running InfiniTime, connect to it, and serve realtime heartrate data over a WebSocket.

This smartly handles and navigates Bluetooth disconnects and other hiccups that you would otherwise need to resolve manually.

This repository needs some cleaning up but it's a small single file incase you need to change something.

## Usage

Run it. It should find your watch and connect automatically. You don't need to pair it.

Data is served at `ws://localhost:8765` as a plaintext number, from 0-255.

## Dependencies

All dependencies should be cross-platform.

- **Bleak**: Bluetooth LE library.
- **Websockets**: Hosts the websocket server.
