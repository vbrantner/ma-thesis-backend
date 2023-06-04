from flask import Flask, Response
import subprocess

app = Flask(__name__)


def generate_frames():
    cmd = "ffmpeg -f avfoundation -framerate 30 -pixel_format yuyv422 -i 0:none -vf scale=1760:1328 -q:v 21 -fps_mode vfr -f mjpeg -"

    # cmd = "ffmpeg -i '0:none' -vf scale=1600:1200 -r 25 -q:v 21 -f mjpeg -"
    p = subprocess.Popen(cmd.split(" "), stdout=subprocess.PIPE)

    data = bytearray()
    while True:
        data.extend(p.stdout.read(1024))
        # start = data.find(b'\xff\xd8')
        # end = data.find(b'\xff\xd9')
        # if start != -1 and end != -1:
        #     jpg = data[start:end+2]
        #     data = data[end+2:]
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + data + b'\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='3000', debug=True)
