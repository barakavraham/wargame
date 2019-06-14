from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user
from app import bcrypt, db
from app.models.user import User
from app.models.army import Army, Upgrade
from app.forms.auth import LoginForm, RegistrationForm

home = Blueprint('home', __name__, template_folder='templates')


@home.route('/', methods=['GET', 'POST'])
def index():
    login_form = LoginForm(prefix='login-form')
    registration_form = RegistrationForm(prefix='registration-form')
    form_button = request.form.get('login') or request.form.get('registration') or ''

    if form_button == 'login-btn' and login_form.validate_on_submit():
        form = login_form
        user = User.query.filter_by(email=form.email.data).first()
        login_user(user, remember=login_form.remember.data)
        next_url = request.args.get('next', 'home.index')
        return redirect(url_for(next_url))

    elif form_button == 'registration-btn' and registration_form.validate_on_submit():
        # UsersMaker()
        form = registration_form
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
        return redirect(url_for('home.index'))

    return render_template('home/index.html',
                           login_form=login_form,
                           registration_form=registration_form,
                           js_vars={
                               'invalidFormButton': form_button
                           })

def UsersMaker():
    names = ["Roanld1", "Killer2" "asa1233", "PoweRanger3", "UnstoppeD3", "Daniel3", "di22232n", "1231233", "REalNam1e", "UnWane3td", "RAN4ANNA", "di1n1oa", "Shirli2", "bosto3n", "1253sssa", "Che1cKCCCCC"]
    for name in names:
        hashed_password = bcrypt.generate_password_hash(name).decode('utf-8')
        user = User(email=f'${name}@gmail.com', password=hashed_password)
        db.session.add(user)
        db.session.commit()
        army = Army(user_id=user.id, name=name)
        db.session.add(army)
        db.session.commit()
        upgrade = Upgrade(army_id=user.id)
        db.session.add(upgrade)
        db.session.commit()