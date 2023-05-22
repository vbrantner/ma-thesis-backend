import base64
import json
import time

import cv2
from flask import Flask, Response
from flask_cors import CORS

app = Flask(__name__)
CORS(app, support_credentials=True)


def capture_frame():
    camera = cv2.VideoCapture(0)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    while True:
        success, frame = camera.read()
        if not success:
            break
        # Convert the frame to JPEG format
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

    camera.release()


@app.route('/video_feed')
def video_feed():
    return Response(capture_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/test')
def test():
    # return example object with json
    data = {
        "testData": "your_test_data_here"
    }
    json_data = json.dumps(data).encode()
    yield Response(json_data, mimetype='application/json')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='3000', debug=True)
