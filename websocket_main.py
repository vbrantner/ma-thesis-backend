import asyncio
import base64
import datetime
import sys
import time

import cv2
import websockets
from turbojpeg import TurboJPEG

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FPS, 40)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 512)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 512)
JPEG = TurboJPEG()


async def take_img():
    ret, frame = cap.read()
    
    jpeg = JPEG.encode(frame, quality=80, jpeg_subsample=2)
    encoded_frame = base64.b64encode(jpeg).decode('utf-8')

    # encode the frame as a JPEG image
    #_, jpeg = cv2.imencode(".jpg", frame)
    # convert the JPEG image to a base64-encoded string
    #jpeg_bytes = jpeg.tobytes()
    #b64_bytes = base64.b64encode(jpeg_bytes)
    #b64_string = b64_bytes.decode("utf-8")
    #size = round(sys.getsizeof(b64_bytes) / (1024 * 1024) * 100) / 100
    #print(f'size of img is {size}')
  

    # send the base64-encoded string over the WebSocket
    return encoded_frame


async def handler(websocket, path):
    # handle incoming messages from the client
    print("client connected")
    try:
        while True:
            start_time = time.perf_counter()
            data = await take_img()
            end_time = time.perf_counter()
            elapsed_time_ms = (end_time - start_time) * 1000
            print(
                f'take_img fn took {elapsed_time_ms:.2f} to execute')

            timestamp = datetime.datetime.now()
            await websocket.send(str(f"{data}, {timestamp}"))
            # await asyncio.sleep(1)

    except websockets.exceptions.ConnectionClosed:
        print('Client disconnected')


async def main():
    # create a WebSocket server on localhost, port 8000
    async with websockets.serve(handler, "", 8000):
        print("WebSocket server started")

        # keep the server running indefinitely
        await asyncio.Future()

# start the event loop

asyncio.run(main())
