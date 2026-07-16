import asyncio
from bleak import BleakClient, BleakScanner
from bleak.backends.characteristic import BleakGATTCharacteristic

HEART_RATE_UUID = "00002a37-0000-1000-8000-00805f9b34fb";

scanner = BleakScanner(service_uuids=[HEART_RATE_UUID]);

heart_rate = 0;

# print(scanner.backend_id);

def heartrateCallback(sender: BleakGATTCharacteristic, data: bytearray):
    print(f"{sender}: {data}")

async def connect() -> BleakClient:
    device = None;

    while device == None:
        # TODO: fallback to this if bleak.exc.BleakDeviceNotFoundError happens
        # foundDevice = None;
        # while foundDevice == None:
        #     foundDevice = await scanner.find_device_by_name("InfiniTime");
        #     print(foundDevice);
        foundDevice = "D9:BE:F4:B9:29:0A";

        device = BleakClient(foundDevice);

        tries = 0;
        while not device.is_connected:
            if tries > 0:
                print("disconnecting");
                await device.disconnect();
            if tries > 1:
                print("unpairing");
                await device.unpair();
            if tries > 5:
                print("waiting 5 seconds")
                await asyncio.sleep(5);

            print("connecting");
            await device.connect();

    return device;

async def ble_main():
    device: BleakClient | None = None;

    while device == None or not device.is_connected:
        device = await connect();

        heart_rate_char = device.services.get_characteristic(HEART_RATE_UUID);
        if heart_rate_char == None:
            raise ValueError("Heart-rate characteristic not found.");

        while device.is_connected:
            data = await device.read_gatt_char(heart_rate_char);
            heart_rate = data[1];
            print(heart_rate);
            await asyncio.sleep(1);

        await device.disconnect();

async def main():
    await asyncio.gather(ble_main());

asyncio.run(main());
