from flask import Flask, send_from_directory

app = Flask(__name__)

OUTPUT_DIR = "/Users/vinzenz/Code/ma-thesis-backend/stream"


@app.route('/stream')
def stream():
    return send_from_directory(OUTPUT_DIR, 'stream.m3u8')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
