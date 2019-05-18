from app import db
from app.models.army import Army
from app.forms.profile import SetArmyNameForm
from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user


profile = Blueprint('profile', __name__, template_folder='templates')


@profile.route("/<army_name>")
@login_required
def index(army_name):
    Army.query.filter_by(name=army_name).first_or_404()
    field = Army.query.filter_by(name=army_name).first().field
    clan = Army.query.filter_by(name=army_name).first().clan
    return render_template('profile/index.html', name=army_name, field=field, clan=clan)


@profile.route('/set_army_name', methods=['GET', 'POST'])
@login_required
def set_army_name():
    if current_user.army.name:
        return redirect(url_for('base.index'))
    form = SetArmyNameForm()
    if form.validate_on_submit():
        current_user.army.name = form.army_name.data
        db.session.commit()
        next_url = request.args.get('next', 'base.index')
        return redirect(url_for(next_url))
    return render_template('profile/set_army_name.html', form=form)
