import asyncio

from state import State
import ble;
import ws;

async def main():
    state = State();
    await asyncio.gather(ble.run(state), ws.host_ws_server(state));

asyncio.run(main());
