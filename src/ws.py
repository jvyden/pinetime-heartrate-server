import asyncio

from aiohttp import web

from state import State

STATE: State = State();

async def handle_root(request: web.Request):
    if request.headers.get("Upgrade", "").lower() == "websocket":
        websocket = web.WebSocketResponse();
        await websocket.prepare(request);

        last_heart_rate = -1;
        while not websocket.closed:
            await websocket.ping();

            if STATE.heart_rate == last_heart_rate:
                await asyncio.sleep(1);
                continue;
            last_heart_rate = STATE.heart_rate;

            await websocket.send_str(str(STATE.heart_rate));
            await asyncio.sleep(1);

        return websocket
    else:
        return web.Response(status=204);

async def start_server(app: web.Application, state: State):
    runner = web.AppRunner(app);
    await runner.setup();

    site = web.TCPSite(runner, state.HOST, state.PORT);
    await site.start();

    return runner;

async def host_ws_server(state: State):
    global STATE;
    STATE = state;

    app = web.Application();
    app.router.add_route("*", "/", handle_root);

    print(f"hosting websocket server on {state.HOST}:{state.PORT}")

    runner = await start_server(app, state);
    try:
        await asyncio.Event().wait()  # run forever
    finally:
        await runner.cleanup()
