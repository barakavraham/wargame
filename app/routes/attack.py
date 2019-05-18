import math
import operator
from app.models.user import User
from app.permissions.permissions import army_name_required
from flask import render_template, Blueprint
from flask_login import login_required

attack = Blueprint('attack', __name__, template_folder='templates')


@attack.route('/')
@attack.route("/<page_num>")
@login_required
@army_name_required
def index(page_num=None):
    page_num = page_num or 1
    page_num = int(page_num)
    users = sorted(User.query.all(), key=operator.attrgetter('army.field'), reverse=True)
    sum_users = math.ceil(len(users)/10)
    users_lists = [users[x:x+10] for x in range(0, sum_users*10, 10)]
    return render_template('attack/index.html', users_lists=users_lists, page_num=page_num, num_lists=sum_users)
