import asyncio

from websockets.asyncio.server import ServerConnection, serve

from state import State

STATE: State = State();

async def ws_client(websocket: ServerConnection):
    last_heart_rate = -1;
    while websocket.close_code == None:
        await websocket.ping();

        if STATE.heart_rate == last_heart_rate:
            await asyncio.sleep(1);
            continue;
        last_heart_rate = STATE.heart_rate;

        await websocket.send(str(STATE.heart_rate), text=True);
        await asyncio.sleep(1);

async def host_ws_server(state: State):
    global STATE;
    STATE = state;

    print(f"hosting websocket server on {state.HOST}:{state.PORT}")

    async with serve(ws_client, state.HOST, state.PORT) as server:
        await server.serve_forever();
