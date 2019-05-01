from flask import render_template, Blueprint
from flask_login import login_required
from app.models import Army
from flask_login import current_user


base = Blueprint('base', __name__, template_folder='templates')


@base.route("/")
@login_required
def index():
    army = Army.query.filter_by(user_id=current_user.id).first()
    return render_template('base.html', army=army)
