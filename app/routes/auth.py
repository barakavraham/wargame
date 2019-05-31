from app.routes.google_auth import google_logout
from flask import url_for, flash, redirect, Blueprint
from flask_login import logout_user

auth = Blueprint('auth', __name__, template_folder='templates')


@auth.route('/logout')
def logout():
    # logout possible google user
    google_logout()
    logout_user()
    flash('You are now logged out')
    return redirect(url_for('home.index'))
