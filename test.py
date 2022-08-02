
from audioop import cross
from cgi import test
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

@app.route('/')
def chat():
    return render_template('chatbox.html')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
