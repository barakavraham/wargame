from flask import render_template, Blueprint
from flask_login import login_required

shop = Blueprint('shop', __name__, template_folder='templates')

@shop.route("/")
@login_required
def index():
    return render_template('shop.html')
