from flask import render_template, Blueprint
from flask_login import login_required
from app.models.army import Army


profile = Blueprint('profile', __name__, template_folder='templates')


@profile.route("/<army_name>")
@login_required
def index(army_name):
    Army.query.filter_by(army_name=army_name).first_or_404()
    field = Army.query.filter_by(army_name=army_name).first().field
    clan = Army.query.filter_by(army_name=army_name).first().clan
    return render_template('profile.html', army_name=army_name, field=field, clan=clan)
