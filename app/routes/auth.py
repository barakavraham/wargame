import os
import json
import functools
from app.config import Auth
from app import app, db, bcrypt
from app.models import User
from app.forms import RegistrationForm, LoginForm
from app.routes.google_auth import google_logout
from flask import render_template, url_for, flash, redirect, request, make_response, session, Blueprint
from flask_login import current_user, login_user, logout_user, login_required

from authlib.client import OAuth2Session
import google.oauth2.credentials
import googleapiclient.discovery
import google

auth = Blueprint('auth', __name__, template_folder='templates')

@auth.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('base.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(email=form.email.data, password=hashed_password, army_name=form.army_name.data)
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=False)
        return redirect(url_for('base.index'))
    return render_template('register.html', form=form)

@auth.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('base.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user.is_google_user:
            flash('This email belongs to a google user')
            return redirect(url_for('auth.login'))
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=False)
            next_url = request.args.get('next', 'base.index')
            return redirect(url_for(next_url))
    return render_template('login.html', form=form)

@auth.route('/logout')
def logout():
    # logout possible google user
    google_logout()
    logout_user()
    flash('You are now logged out')
    return redirect(url_for('auth.login'))
