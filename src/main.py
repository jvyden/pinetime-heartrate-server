import asyncio

from state import State
import ble;
import ws;
import osc;

async def main():
    state = State();
    await asyncio.gather(ble.run(state), ws.host_ws_server(state), osc.start_osc_sender(state));

asyncio.run(main());
