from flask import render_template, Blueprint
from flask_login import login_required
from app.models.army import Army


profile = Blueprint('profile', __name__, template_folder='templates')


@profile.route("/<name>")
@login_required
def index(name):
    Army.query.filter_by(name=name).first_or_404()
    field = Army.query.filter_by(name=name).first().field
    clan = Army.query.filter_by(name=name).first().clan
    return render_template('profile.html', name=name, field=field, clan=clan)
