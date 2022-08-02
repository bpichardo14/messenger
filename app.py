from audioop import cross
from crypt import methods
from email.utils import format_datetime
from click import confirm
from flask import Flask, render_template, url_for, redirect, flash
from flask_socketio import SocketIO, emit
from forms import RegistrationForm, LoginForm
import os
from enum import unique
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, logout_user, LoginManager, login_required, current_user
from flask_migrate import Migrate
from flask_cors import CORS, cross_origin


# create flask instance
app = Flask(__name__)

# create socketio instance 
socketio = SocketIO(app)

# initilize databse
db = SQLAlchemy(app)
migrate = Migrate(app, db)
CORS(app)
app.config['SECRET_KEY'] = 'your-key'
# create database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

# Flask login stuff 
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    name = db.Column(db.String(50), nullable=False, unique=False)
    last_name = db.Column(db.String(50), nullable=False, unique=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False, unique=True)


@app.route('/')
@cross_origin()
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST', 'GET'])
def register():

    username = None
    name = None
    last_name = None
    email = None
    password = None 
    confirm_password = None

    form = RegistrationForm()

    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        confirm_password = form.confirm_password.data

        user = Users(name=form.name.data, last_namae=form.last_name.data, username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
    

    return render_template('register.html', form=form, username=username, email=email, password=password, 
                                            confirm_password=confirm_password)

@login_manager.user_loader
def load_user(id):
    return Users.query.get(int(id))


# login page 
@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user:
            if  Users.query.filter_by(password=form.password.data).first():
                login_user(user)
                flash('Login Successful')
                return redirect(url_for('index'))
            else:
                flash('Wrong Password -  try again')
        else:
            flash('This username does not exist - try again')

    return render_template('login.html', form=form)

@app.route('/profile')
def profile():
    return render_template('profile.html')


@login_required
@app.route('/logout', methods=['POST', 'GET'])
def logout():
    logout_user()
    flash('You have logged out')
    redirect(url_for('login'))

# 3. listens for message sent by client
@socketio.on('message')
def message_handler(data):
    print('message sent to server')
    emit('new_message', data) # calls whoever is listening of new_message


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')

