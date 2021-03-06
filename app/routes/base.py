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
        "coin": UserResources(current_user.army.coin, 'coin'),
        "metal": UserResources(current_user.army.metal, 'metal'),
        "wood": UserResources(current_user.army.wood, 'wood'),
        "field": UserResources(current_user.army.field, 'field'),
        "diamond": UserResources(current_user.army.diamond, 'diamond'),
    }
    return user_resources


@base.route("/")
@login_required
@army_name_required
def index():
    user_resources = get_user_resources()
    return render_template('base/index.html', user_resources=user_resources)
