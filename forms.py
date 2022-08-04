from tokenize import String
from flask_wtf import FlaskForm
# from h11 import Data
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flask_wtf.file import FileField

class RegistrationForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()] )
    
    last_name =StringField('last_name', validators=[DataRequired()])

    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])

    email = StringField('Email',
                        validators=[DataRequired(), Email()])

    password = PasswordField('Password', validators=[DataRequired()])

    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])

    profile_pic = FileField("Profile Picture")

    submit = SubmitField('Sign Up', validators=[DataRequired()])

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])

    password = PasswordField('Password', validators=[DataRequired()])

    submit = SubmitField('Submit', validators=[DataRequired()])
