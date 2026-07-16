# PineTime Heartrate Server
A program to find a PineTime watch running InfiniTime, connect to it, and serve realtime heartrate data over a WebSocket.

This smartly handles and navigates Bluetooth disconnects and other hiccups that you would otherwise need to resolve manually.

The code needs some cleaning up to facilitate custom ports or other devices, but it's a small single file incase you need to change the constants. This technically works with anything exposing heart rate data over BLE (characteristic `2a37`) if you'd like to adapt it to your watch.

## Usage

Run it. `python3 src/main.py`

Data is served at `ws://localhost:8765` as a plaintext number, ranging from 0-255.

Provided Bluetooth gods are on your side today, it should just find your watch and connect automatically. You don't need to pair it. This doesn't mean you don't need to connect manually, I mean you literally do not need to enter the PIN or anything to access the data.

Is that secure? Not really.

Is it my problem? No.

Can't you just shove whoever's reading your data away because they're within 3 feet? Yeah.

## Dependencies

All dependencies should be cross-platform.

- **Bleak**: Bluetooth LE library.
- **Websockets**: Hosts the websocket server.
