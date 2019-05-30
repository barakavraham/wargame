from app import db, bcrypt
from app.models.user import User
from app.models.army import Army, Upgrade
from app.forms.auth import RegistrationForm, LoginForm
from app.routes.google_auth import google_logout
from flask import url_for, flash, redirect, request, Blueprint
from flask_login import current_user, login_user, logout_user


auth = Blueprint('auth', __name__, template_folder='templates')


@auth.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('base.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        army = Army(user_id=user.id, name=form.army_name.data)
        db.session.add(army)
        db.session.commit()
        upgrade = Upgrade(army_id=user.id)
        db.session.add(upgrade)
        db.session.commit()
        login_user(user, remember=False)
        return redirect(url_for('base.index'))
    return redirect(url_for('home.index'))


@auth.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('base.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user.is_google_user:
            flash('This email belongs to a google user')
            return redirect(url_for('home.index'))
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=False)
            next_url = request.args.get('next', 'base.index')
            return redirect(url_for(next_url))
    return redirect(url_for('home.index'))


@auth.route('/logout')
def logout():
    # logout possible google user
    google_logout()
    logout_user()
    flash('You are now logged out')
    return redirect(url_for('home.index'))
