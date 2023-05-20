import asyncio
import base64
import os
import time
import websockets
import cv2

# set the directory containing the BMP images
images_dir = "/home/pi/backend/images"

# get the list of BMP image filenames in the directory
image_filenames = [f for f in os.listdir(images_dir) if f.endswith(".bmp")]
image_filenames.sort()

# set the frame rate for serving the images over the WebSocket
fps = 30

# set the sleep time between each frame to achieve the desired frame rate
sleep_time = 1 / fps

async def send_images(websocket, path):
    try:
        # loop through each image and send it over the WebSocket
        for filename in image_filenames:
            # read the image file
            img = cv2.imread(os.path.join(images_dir, filename))

            # encode the image as a JPEG image
            _, jpeg = cv2.imencode(".jpg", img)

            # convert the JPEG image to a base64-encoded string
            jpeg_bytes = jpeg.tobytes()
            b64_bytes = base64.b64encode(jpeg_bytes)
            b64_string = b64_bytes.decode("utf-8")

            # send the base64-encoded string over the WebSocket
            await websocket.send(str(b64_string))

            # wait for the specified time to achieve the desired frame rate
            await asyncio.sleep(sleep_time)

    except websockets.exceptions.ConnectionClosed:
        print('Client disconnected')

async def main():
    # create a WebSocket server on localhost, port 8000
    async with websockets.serve(send_images, "", 8000):
        print("WebSocket server started")

        # keep the server running indefinitely
        await asyncio.Future()

# start the event loop
asyncio.run(main())

