import math
import operator
from app.models.user import User
from app.permissions.permissions import army_name_required
from flask import render_template, Blueprint
from flask_login import login_required, current_user

attack = Blueprint('attack', __name__, template_folder='templates')


@attack.route('/')
@attack.route("/<page_num>")
@login_required
@army_name_required
def index(page_num=None):
    if page_num is not None:
        page_num = int(page_num)
    users = sorted(User.query.all(), key=operator.attrgetter('army.field'), reverse=True)
    sum_users = math.ceil(len(users)/10)
    users_lists = [users[x:x+10] for x in range(0, sum_users*10, 10)]
    if page_num is None or page_num <= 0:
        for users_list in users_lists:
            if current_user in users_list:
                page_num = users_lists.index(users_list) + 1
                break
    return render_template('attack/index.html', users_lists=users_lists, page_num=page_num, num_lists=sum_users)
