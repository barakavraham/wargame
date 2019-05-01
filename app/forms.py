from app.models import User
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app import bcrypt


class RegistrationForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                        validators=[DataRequired(), Length(min = 6, max = 32)])
    confirm_password = PasswordField('Confirm Paswword',
                        validators=[DataRequired(), EqualTo('password')])
    army_name = StringField('Army Name', 
                        validators=[DataRequired(), Length(min = 3, max = 24)])
    submit = SubmitField('Sign up')

    @staticmethod
    def validate_army_name(self, army_name):
        user = User.query.filter_by(army_name=army_name.data).first()
        if user:
            raise ValidationError('This army name is already taken')

    @staticmethod
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email is already taken')

    @staticmethod
    def validate_army_name(self, army_name):
        if not army_name.data.isalnum():
            raise ValidationError('Army name must contain english letters or numbers')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                        validators=[DataRequired(), Length(min = 6, max = 32)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')

    @staticmethod
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError("Invaild email or password")
        elif not bcrypt.check_password_hash(user.password, self.password.data):
            raise ValidationError("Invaild email or password")




