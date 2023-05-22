from flask import Flask, render_template
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import cv2
import base64
from threading import Thread, Event

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

thread = Thread()
thread_stop_event = Event()


class VideoStreamThread(Thread):
    def __init__(self):
        # self.delay = 0.1
        super(VideoStreamThread, self).__init__()

    def getImage(self):
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        ret, jpeg = cv2.imencode('.jpg', frame)
        return base64.b64encode(jpeg.tobytes())

    def run(self):
        while not thread_stop_event.isSet():
            image = self.getImage()
            # socketio.emit('new_frame', {'image': 'test123'}, namespace='/test')
            socketio.emit('new_frame', {'image': 'data:image/jpg;base64,' + image.decode()}, namespace='/test')
            socketio.sleep(1/40)


@socketio.on('connect', namespace='/test')
def test_connect():
    global thread
    print('Client connected')

    if not thread.is_alive():
        print("Starting Thread")
        thread = VideoStreamThread()
        thread.start()


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')


if __name__ == '__main__':
    socketio.run(app, port=8080)
