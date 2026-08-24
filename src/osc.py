import asyncio

from pythonosc import udp_client

from state import State


async def start_osc_sender(state: State):
    client = udp_client.SimpleUDPClient(state.OSC_HOST, state.OSC_PORT);

    while state.OSC_ENABLE:
        client.send_message("/avatar/parameters/hr_connected", state.heart_rate > -1);

        if state.heart_rate > 0:
            client.send_message("/avatar/parameters/hr_percent", state.heart_rate / 200);

        await asyncio.sleep(1);
