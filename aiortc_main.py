import asyncio
import cv2
import numpy as np
from av import VideoFrame
from aiortc import MediaStreamTrack, RTCPeerConnection, RTCSessionDescription, VideoStreamTrack
from aiortc.contrib.media import MediaBlackhole, MediaPlayer, MediaRecorder

class VideoTransformTrack(MediaStreamTrack):
    """
    A video stream track that takes frames from a video capture and yields them to consumers.
    """
    kind = "video"

    def __init__(self, track):
        super().__init__()  # don't forget this!
        self.track = track

    async def recv(self):
        frame = await self.track.recv()

        # perform image transformation
        img = frame.to_ndarray(format="bgr24")
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        new_frame = VideoFrame.from_ndarray(img, format="bgr24")
        new_frame.pts = frame.pts
        new_frame.time_base = frame.time_base
        return new_frame

async def run(pc):
    player = MediaPlayer('/dev/video0', format='v4l2', options={'video_size': '640x480'})
    if player.video:
        local_video = VideoTransformTrack(player.video)
        pc.addTrack(local_video)

    @pc.on("track")
    def on_track(track):
        print("Track %s received" % track.kind)

    return pc

if __name__ == "__main__":
    pc = RTCPeerConnection()
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(run(pc))
    except Exception as e:
        print(str(e))
    finally:
        loop.run_until_complete(pc.close())
