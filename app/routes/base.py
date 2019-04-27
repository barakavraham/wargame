from flask import render_template, Blueprint
from flask_login import login_required, current_user
from app.routes.google_auth import get_user_info

base = Blueprint('base', __name__, template_folder='templates')

@base.route("/")
@login_required
def index():
    return render_template('base.html')

