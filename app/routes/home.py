from flask import render_template, Blueprint
from app.forms.auth import LoginForm, RegistrationForm

home = Blueprint('home', __name__, template_folder='templates')


@home.route('/')
def index():
    login_form = LoginForm(prefix='login-form')
    registration_form = RegistrationForm(prefix='registration-form')
    return render_template('home/index.html', login_form=login_form, registration_form=registration_form)
