from app.models.user import User
from app.models.army import Army
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app import bcrypt


class RegistrationForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()],
                        render_kw={'placeholder': 'Email', 'type': 'email', 'id': 'registration-email'})
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(min=6, max=32)],
                             render_kw={'placeholder': 'Password', 'id': 'registration-password'})
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')],
                                     render_kw={'placeholder': 'Confirm Password',
                                                'id': 'registration-confirm-password'})
    army_name = StringField('Army Name',
                            validators=[DataRequired(), Length(min=3, max=16)],
                            render_kw={'placeholder': 'Army Name', 'id': 'registration-army-name'})

    @staticmethod
    def validate_army_name(_, army_name):
        army = Army.query.filter_by(name=army_name.data).first()
        if army:
            raise ValidationError('This army name is already taken')
        if not army_name.data.isalnum():
            raise ValidationError('Army name must contain only numbers and letters')

    @staticmethod
    def validate_email(_, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email is already taken')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()],
                        render_kw={'placeholder': 'Email', 'type': 'email', 'id': 'login-email'})
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(min=6, max=32)],
                             render_kw={'placeholder': 'Password', 'id': 'login-password'})
    remember = BooleanField('Remember me')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError("Invalid email or password")
        elif user.is_google_user:
            raise ValidationError("This email belongs to a google user")
        elif not bcrypt.check_password_hash(user.password, self.password.data):
            raise ValidationError("Invalid email or password")
