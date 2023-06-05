from flask import Flask, render_template, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/stream/<path:path>')
def stream(path):
    return send_from_directory('/home/vinzenz/ma-thesis-backend/stream', path)

if __name__ == '__main__':
      app.run(host='0.0.0.0', port='3000', debug=True)