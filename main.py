from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit
from modules import youtube
import sys, json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/courses', methods=['GET', 'POST'])
def courses():
    videos = []
    if request.method == 'POST':
        data = request.form
        print(data, file=sys.stderr)
        keyword = data.get('search')
        videos = json.loads(youtube(keyword, 10))
    return render_template('courses.html', videos = videos)

@app.route('/present')
def present():
    return render_template('present.html')


@app.route('/listen')
def listen():
    return render_template('listen.html')


@socketio.on('message')
def handle_message(msg):
    print('Message: ' + msg)
    send(msg, broadcast=True)


if __name__ == '__main__':
    socketio.run(app, debug=True)
