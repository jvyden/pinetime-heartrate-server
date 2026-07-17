import asyncio
from pathlib import Path
from bleak import BleakClient, BleakScanner
from bleak.backends.device import BLEDevice
from bleak.exc import BleakDeviceNotFoundError
from websockets.asyncio.server import ServerConnection, serve

HEART_RATE_UUID = "00002a37-0000-1000-8000-00805f9b34fb";
LAST_ADDRESS = Path("lastaddress.txt");

scanner = BleakScanner(service_uuids=[HEART_RATE_UUID]);

global heart_rate;
heart_rate = -1;

async def find_device(skip_existing: bool) -> BLEDevice | str:
    if not skip_existing and LAST_ADDRESS.exists():
        file = LAST_ADDRESS.open("r");
        last_address = file.readline();
        print("attempting existing device % s" % last_address)
        if len(last_address) > 0:
            return last_address.strip();


    foundDevice = None;
    while foundDevice == None:
        print("scanning for device");
        foundDevice = await scanner.find_device_by_name("InfiniTime");

    print("found device % s" % foundDevice.address);

    file = LAST_ADDRESS.open("w");
    file.write(foundDevice.address)

    return foundDevice;

async def connect() -> BleakClient:
    device = None;

    while device == None:
        foundDevice = await find_device(False);

        device = BleakClient(foundDevice);

        tries = 0;
        while not device.is_connected:
            try:
                if tries > 0:
                    print("disconnecting");
                    await device.disconnect();
                if tries > 1:
                    print("unpairing");
                    await device.unpair();
                if tries > 5:
                    print("waiting 5 seconds");
                    await asyncio.sleep(5);

                print("connecting");
                async with asyncio.timeout(10):
                    await device.connect();
            except BleakDeviceNotFoundError:
                foundDevice = await find_device(True);
            except Exception as e:
                print(e);

            tries += 1;

    return device;

async def ble_main():
    device: BleakClient | None = None;

    while device == None or not device.is_connected:
        device = await connect();
        print("connected")

        heart_rate_char = device.services.get_characteristic(HEART_RATE_UUID);
        if heart_rate_char == None:
            raise ValueError("Heart-rate characteristic not found.");

        while device.is_connected:
            try:
                data = await device.read_gatt_char(heart_rate_char);
                global heart_rate;
                heart_rate = data[1];
                print(heart_rate);
            except:
                await device.disconnect();
            await asyncio.sleep(1);

        await device.disconnect();

async def ws_client(websocket: ServerConnection):
    last_heart_rate = -1;
    while websocket.close_code == None:
        await websocket.ping();

        if heart_rate == last_heart_rate:
            await asyncio.sleep(1);
            continue;
        last_heart_rate = heart_rate;

        await websocket.send(str(heart_rate), text=True);
        await asyncio.sleep(1);

async def ws_main():
    async with serve(ws_client, "localhost", 8765) as server:
        await server.serve_forever();

async def main():
    await asyncio.gather(ble_main(), ws_main());

asyncio.run(main());
