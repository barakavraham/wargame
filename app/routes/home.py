from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user
from app import db
from app.utils.user import create_user
from app.models.user import User
from app.models.army import Army, Upgrade
from app.forms.auth import LoginForm, RegistrationForm

home = Blueprint('home', __name__, template_folder='templates')


@home.route('/', methods=['GET', 'POST'])
def index():
    login_form = LoginForm()
    registration_form = RegistrationForm()

    return render_template('home/index.html',
                           login_form=login_form,
                           registration_form=registration_form)
