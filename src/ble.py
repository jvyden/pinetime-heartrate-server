import asyncio
import time
from pathlib import Path

from bleak import BleakClient, BleakScanner
from bleak.backends.device import BLEDevice
from bleak.exc import BleakDeviceNotFoundError

from state import State

HEART_RATE_UUID = "00002a37-0000-1000-8000-00805f9b34fb";
LAST_ADDRESS = Path("lastaddress.txt");

scanner = BleakScanner(service_uuids=[HEART_RATE_UUID]);

async def find_device(state: State, skip_existing: bool) -> BLEDevice | str:
    if not skip_existing and LAST_ADDRESS.exists():
        with LAST_ADDRESS.open("r") as file:
            last_address = file.readline();
            print(f"attempting existing device {last_address}")
            if len(last_address) > 0:
                return last_address.strip();


    foundDevice = None;
    while foundDevice == None:
        print(f"scanning for {state.DEVICE_NAME}");
        foundDevice = await scanner.find_device_by_name(state.DEVICE_NAME);

    print(f"found device {foundDevice.address}");

    with LAST_ADDRESS.open("w") as file:
        file.write(foundDevice.address)

    return foundDevice;

async def connect(state: State) -> BleakClient:
    device = None;

    while device == None:
        foundDevice = await find_device(state, False);

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
                foundDevice = await find_device(state, True);
            except Exception as e:
                print(e);

            tries += 1;

    return device;

async def run(state: State):
    device: BleakClient | None = None;

    while device == None or not device.is_connected:
        device = await connect(state);
        print("connected")

        heart_rate_char = device.services.get_characteristic(HEART_RATE_UUID);
        if heart_rate_char == None:
            raise ValueError("Heart-rate characteristic not found.");

        if not device.is_connected:
            return;

        await align_polling(device, state, heart_rate_char);

        # actual polling loop
        while device.is_connected:
            try:
                await poll_hr(device, state, heart_rate_char);
                state.last_heart_rate = state.heart_rate;
            except:
                await device.disconnect();

            await asyncio.sleep(1);

        await device.disconnect();

async def poll_hr(device: BleakClient, state: State, char):
    data = await device.read_gatt_char(char);
    state.heart_rate = data[1];

    state.update_event.set();
    state.update_event.clear();

    if state.last_heart_rate != state.heart_rate:
        print(f"{state.heart_rate}BPM");

    state.last_valid_contact = time.time();

async def align_polling(device: BleakClient, state: State, char):
    print("fast polling until aligned to reduce latency")

    align_start = time.time();

    # get an initial hr value in
    await poll_hr(device, state, char);
    state.last_heart_rate = state.heart_rate;

    # poll as fast as possible until we get an update
    # this should reduce latency a bit by aligning us when the heart scanner updates on the watch
    # but in doing so still not polling aggressively
    while time.time() - align_start < 15:
        await poll_hr(device, state, char);
        if state.last_heart_rate != state.heart_rate:
            return

    print("giving up on fast polling, there will be a bit more delay in heart rate changes");
