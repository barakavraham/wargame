from app.models.user import User
from app.utils.user import create_user
from app.forms.auth import LoginForm, RegistrationForm
from app.routes.google_auth import google_logout
from flask import Blueprint, url_for, flash, redirect, request, render_template
from flask_login import login_user, logout_user

auth = Blueprint('auth', __name__, template_folder='templates')


@auth.route('/login', methods=['POST'])
def login():
    form = LoginForm(**request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        login_user(user, remember=form.remember.data)
        next_url = request.args.get('next', 'home.index')
        return redirect(url_for(next_url))
    return render_template('home/index.html',
                           login_form=form,
                           registration_form=RegistrationForm(),
                           js_vars={
                               'invalidFormButton': 'login-btn'
                           })


@auth.route('/register', methods=['POST'])
def register():
    form = RegistrationForm(**request.form)
    if form.validate_on_submit():
        user = create_user(email=form.email.data, password=form.password.data, army_name=form.army_name.data)
        login_user(user, remember=False)
        return redirect(url_for('home.index'))
    return render_template('home/index.html',
                           login_form=LoginForm(),
                           registration_form=form,
                           js_vars={
                               'invalidFormButton': 'registration-btn'
                           })

@auth.route('/logout')
def logout():
    # logout possible google user
    google_logout()
    logout_user()
    flash('You are now logged out')
    return redirect(url_for('home.index'))
