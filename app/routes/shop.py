from app.utils.shop import SHOP_ITEMS, TECH_UPGRADES
from app.permissions.permissions import army_name_required
from flask import render_template, Blueprint
from flask_login import login_required

shop = Blueprint('shop', __name__, template_folder='templates')


@shop.route("/")
@login_required
@army_name_required
def index():
    return render_template('shop/index.html',
                           shop_items=SHOP_ITEMS,
                           tech_upgrades=TECH_UPGRADES)
