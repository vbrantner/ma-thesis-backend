import json
import time

import cv2
from flask import Flask, Response
from flask_cors import CORS
import turbojpeg as tj

app = Flask(__name__)
CORS(app, support_credentials=True)


compressor = tj.TurboJPEG()
def capture_frame(quality=90):
    camera = cv2.VideoCapture(0)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1024)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 1024)
    
    # Create TurboJPEG compressor
    
    while True:
        start_time = time.time()  # Record start time

        success, frame = camera.read()
        if not success:
            break
        
        # Convert the frame to JPEG format using TurboJPEG
        compressed_frame = compressor.encode(frame, quality=quality)
        
        # Calculate image size
        image_size = len(compressed_frame) / 1024  # Convert to kilobytes
        
        print(f"Image size: {image_size:.2f} KB")
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + compressed_frame + b'\r\n\r\n')
        end_time = time.time()  # Record end time
        execution_time = end_time - start_time
        print(f"Execution time: {execution_time:.4f} seconds") 
    
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
