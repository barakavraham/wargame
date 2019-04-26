from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationForm(FlaskForm):
    username = StringField('Username', 
                        validators=[DataRequired(), Length(min = 3, max = 10)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                        validators=[DataRequired(), Length(min = 6, max = 15)])
    confirm_password = PasswordField('Confirm Paswword',
                        validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign up')

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email])
    password = PasswordField('Password',
                        validators=[DataRequired(), Length(min = 6, max = 15)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')