from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)


@app.route('/')
def index():
    return render_template('index.html')

# 3. listens for message sent by client
@socketio.on('message')
def message_handler(data):
    print('message sent to server')
    emit('new_message', data) # calls whoever is listening of new_message


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')