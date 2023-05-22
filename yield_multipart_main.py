import base64
import json
import time

import cv2
from flask import Flask, Response
from flask_cors import CORS

app = Flask(__name__)
CORS(app, support_credentials=True)


def generate():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    while True:
        ret, frame = cap.read()
        if ret:
            ret, jpeg = cv2.imencode('.jpg', frame)
            b64_bytes = base64.b64encode(jpeg)
            b64_string = b64_bytes.decode("utf-8")
            if ret:
                data = {
                    "imgData": b64_string,
                    "timestamp": time.time(),
                    "testData": "your_test_data_here"
                }
                json_data = json.dumps(data).encode()
                yield json_data


@app.route('/')
def video_feed():
    return Response(generate(), mimetype='application/json')


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
