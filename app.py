from crypt import methods
from click import confirm
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from forms import RegistrationForm
import os

# create flask instance
app = Flask(__name__)

# create socketio instance 
socketio = SocketIO(app)

app.config['SECRET_KEY'] = 'your-key'


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST', 'GET'])
def register():

    username = None
    email = None
    password = None 
    confirm_password = None

    form = RegistrationForm()

    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        confirm_password = form.confirm_password.data



    return render_template('register.html', form=form, username=username, email=email, password=password, 
                                            confirm_password=confirm_password)
    


# 3. listens for message sent by client
@socketio.on('message')
def message_handler(data):
    print('message sent to server')
    emit('new_message', data) # calls whoever is listening of new_message


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')

