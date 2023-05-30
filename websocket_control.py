import asyncio
import datetime
import time

import websockets


async def handler(websocket, path):
    print("New client connected")
    while True:
        try:
            message = await websocket.recv()
            # Process the received message
            # Here, we simply send the received value back to the client
            await websocket.send(message)
        except websockets.exceptions.ConnectionClosed:
            break


async def main():
    # create a WebSocket server on localhost, port 8000
    async with websockets.serve(handler, "", 8000):
        print("WebSocket server started")

        # keep the server running indefinitely
        await asyncio.Future()

# start the event loop

asyncio.run(main())
