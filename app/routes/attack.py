from flask import render_template, Blueprint
from flask_login import login_required
from app.models import User
import operator
import math

attack = Blueprint('attack', __name__, template_folder='templates')


@attack.route("/<page_num>")
@login_required
def index(page_num):
    page_num = int(page_num)
    users = sorted(User.query.all(), key=operator.attrgetter('army.field'), reverse=True)
    sum_users = math.ceil(len(users)/10)
    users_lists = [users[x:x+10] for x in range(0, sum_users*10+1, 5)]
    return render_template('attack.html', users_lists=users_lists, page_num=page_num, num_lists=sum_users)
