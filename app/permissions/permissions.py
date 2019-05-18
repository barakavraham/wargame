from functools import wraps
from flask import request, redirect, url_for, flash
from flask_login import current_user


def army_name_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.army.name:
            flash('You must have an army name to access this page')
            return redirect(url_for('profile.set_army_name', next=request.endpoint))
        return f(*args, **kwargs)
    return decorated_function
