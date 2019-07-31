from app.models.army import BattleResult
from app.models.user import Mail
from app.permissions.permissions import army_name_required
from flask import Blueprint, render_template
from flask_login import login_required, current_user

mail = Blueprint('mail', __name__, template_folder='templates')


@mail.route('/')
@login_required
@army_name_required
def index():
    attacker_battle_results = (BattleResult.query
                               .filter_by(attacker_army_id=current_user.army.id)
                               .order_by(BattleResult.timestamp.desc()).all())
    attacked_battle_results = (BattleResult.query
                               .filter_by(attacked_army_id=current_user.army.id)
                               .order_by(BattleResult.timestamp.desc()).all())
    user_mails_received = (Mail.query.filter_by(recipient_id=current_user.id)
                           .order_by(Mail.timestamp.desc()).all())

    return render_template('mail/index.html',
                           attacker_battle_results=attacker_battle_results,
                           attacked_battle_results=attacked_battle_results,
                           user_mails_received = user_mails_received)


@mail.app_template_filter('result_to_class_name')
def jinja_result_to_class_name(did_attacker_win, is_attacker):
    if is_attacker:
        if did_attacker_win is True:
            return 'success'
        elif did_attacker_win is False:
            return 'danger'
        else:
            return 'warning'
    else:
        if did_attacker_win is True:
            return 'danger'
        elif did_attacker_win is False:
            return 'success'
        else:
            return 'warning'
