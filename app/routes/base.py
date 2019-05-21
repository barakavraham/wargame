from dataclasses import dataclass
from flask import render_template, Blueprint
from flask_login import login_required, current_user
from app.permissions.permissions import army_name_required

base = Blueprint('base', __name__, template_folder='templates')


@dataclass
class UserResources:
    amount: int
    picture: str


def get_user_resources():
    user_resources = {
        "Coins": UserResources(current_user.army.coin, 'coin'),
        "Metal": UserResources(current_user.army.metal, 'metal'),
        "Wood": UserResources(current_user.army.wood, 'wood'),
        "field": UserResources(current_user.army.field, 'field')
    }
    return user_resources


@base.route("/")
@login_required
@army_name_required
def index():
    user_resources = get_user_resources()
    return render_template('base/index.html', user_resources=user_resources)
