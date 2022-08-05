from audioop import cross
from crypt import methods
from email.utils import format_datetime
from pydoc import render_doc
from click import confirm
from flask import Flask, render_template, url_for, redirect, flash, session, request
from flask_socketio import SocketIO, emit
from forms import RegistrationForm, LoginForm
import os
from enum import unique
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, logout_user, LoginManager, login_required, current_user
from flask_migrate import Migrate
from flask_cors import CORS, cross_origin
from flask_session import Session
from werkzeug.utils import secure_filename
import uuid as uuid
from apicall import connect_to_spotify


# create flask instance
app = Flask(__name__)

# app.config["SESSION_PERMANENT"] = False
# app.config["SESSION_TYPE"] = "filesystem"

# # set up session
# session = Session(app)

# create socketio instance 
socketio = SocketIO(app)

CORS(app)
app.config['SECRET_KEY'] = '1a118f8864390243e3381fead7467eee'
# create database
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://nqbjwsvjatjsqi:ef1f39db0389f0fab79fd22643b8452afbc56f34bd9b497fd4b0ed9e4c6ecf90@ec2-44-205-64-253.compute-1.amazonaws.com:5432/d67tjlvrcobtqe'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
# Flask login stuff 
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# save image
UPLOAD_FOLDER = 'static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    name = db.Column(db.String(50), nullable=False, unique=False)
    last_name = db.Column(db.String(50), nullable=False, unique=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False, unique=False)
    profile_pic = db.Column(db.String(), nullable=True)


@app.route('/chat')
@cross_origin()
@login_required
def index():
    return render_template('index.html')

# REGISTER PAGE
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

        user = Users(name=form.name.data, last_name=form.last_name.data, username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
    

    return render_template('register.html', form=form, username=username, email=email, password=password, 
                                            confirm_password=confirm_password)

@login_manager.user_loader
def load_user(id):
    return Users.query.get(int(id))


# LOGIN PAGE 
@app.route('/', methods=['POST', 'GET'])
def login():
    # session.clear()
    form = LoginForm()

    if form.validate_on_submit():
        # session['username']=form.username.data

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


# PROFILE PAGE
@app.route('/profile', methods=['POST', 'GET'])
@login_required
def profile():
    form = RegistrationForm()
    id = current_user.id
    user_to_update = Users.query.get_or_404(id)
    if request.method == 'POST':
        song = connect_to_spotify(current_user.username)
        user_to_update.name = request.form['name']
        user_to_update.last_name = request.form['last_name']
        user_to_update.username = request.form['username']
        user_to_update.email = request.form['email']
        # print(request.files['profile_pic'])
        
        if request.files['profile_pic']:

            user_to_update.profile_pic = request.files['profile_pic']

            pic_filename = secure_filename(user_to_update.profile_pic.filename)

            pic_name = str(uuid.uuid1()) + "_" + pic_filename

            saver = request.files['profile_pic']

            user_to_update.profile_pic = pic_name

            try:
                db.session.commit()
                print('commiting1')
                saver.save(os.path.join(app.config['UPLOAD_FOLDER'], pic_name))
                flash("User Updated Successfully!")
                return render_template("profile.html", 
					form=form,
					user_to_update = user_to_update)
            except:
                print('erro1')
                flash("Error!  Looks like there was a problem...try again!")
                return render_template("profile.html", 
					form=form,
					user_to_update = user_to_update)
        else:
            print('commiting2')
            db.session.commit()
            flash("User Updated Successfully!")
            return render_template("profile.html", 
				form=form, 
				user_to_update = user_to_update)
    else:
        print('no commit')
        return render_template("profile.html", 
				form=form,
				user_to_update = user_to_update,
				id = id, song=song)
    return render_template('profile.html')



# LOGOUT
@app.route('/logout', methods=['POST', 'GET'])
@login_required
def logout():
    logout_user()
    flash('You have logged out')
    return redirect(url_for('login'))


# UPDATE PROFILE
@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    form = RegistrationForm()
    user_to_update = Users.query.get_or_404(id)
    if request.method == 'POST':
        user_to_update.name = request.form['name']
        user_to_update.last_name = request.form['last_name']
        user_to_update.username = request.form['username']
        user_to_update.email = request.form['email']
        
        try:
            db.session.commit()
            flash('User updated successfuly')
            return render_template('update.html', form=form, user_to_update=user_to_update)
        except:
            flash('Error! Looks like there was problem, but try again!')
            return render_template('update.html', form=form, user_to_update=user_to_update)
    else:
        return render_template('update.html', form=form, user_to_update=user_to_update)

# # CONNECT TO SPOTIFY
# @app.route('/spotify', methods=['POST', 'GET'])
# def connect_to_spotify():
#     form = RegistrationForm()
#     CLIENT_ID = '4d7fed3f38454c82abe7000ed50f7a13'
#     CLIENT_SECRET = '9748fcc8cf064b7eb259f2adf4f43abe'

#     username = "pichardobrayan"
#     scope = "user-read-currently-playing"
#     redirect_uri = 'http://localhost:5000/callback/'

#     token = util.prompt_for_user_token(username, scope, CLIENT_ID, CLIENT_SECRET, redirect_uri)

#     sp = spotipy.Spotify(auth=token)
#     currentsong = sp.currently_playing()

#     song_name = currentsong['item']['name']
#     song_artist = currentsong['item']['artists'][0]['name']
#     listening_to = "Now playing {} by {}".format(song_name, song_artist)

#     return render_template('profile.html', form=form, listening_to=listening_to)

# 3. listens for message sent by client
@socketio.on('message')
def message_handler(data):
    print('message sent to server')
    emit('new_message', data, broadcast=True) # calls whoever is listening of new_message


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')

