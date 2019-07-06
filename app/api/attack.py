import json
from flask import render_template, abort, url_for
from flask_restful import Resource, reqparse
from app import db
from app.models.user import User
from app.models.army import BattleResult
from app.api import base_api, SubpathApi
from app.permissions.permissions import login_required_for_api
from app.utils.attack import attack, ATTACK_COSTS

subpath_api = SubpathApi(base_api, '/attack', 'attack')


class OpenProfileWindowAPI(Resource):
    decorators = [login_required_for_api]

    @staticmethod
    def get(user_id):
        user = User.query.get_or_404(user_id)
        return render_template('attack/profile.html', user=user)


subpath_api.add_resource(OpenProfileWindowAPI,
                         '/user_profile/<int:user_id>',
                         endpoint='user_profile')


class AttackAPI(Resource):
    decorators = [login_required_for_api]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('attacker_user_id', type=int, required=True)
        self.reqparse.add_argument('attacked_user_id', type=int, required=True)
        self.reqparse.add_argument('weapon_types', type=str)
        super(AttackAPI, self).__init__()

    @staticmethod
    def can_attack(attacker_army, weapon_types):
        return attacker_army.turns >= sum([ATTACK_COSTS[weapon_type] for weapon_type in weapon_types])

    @staticmethod
    def validate_weapon_types(weapon_types):
        return isinstance(weapon_types, list) and all([weapon_type in ATTACK_COSTS for weapon_type in weapon_types])

    def post(self):
        args = self.reqparse.parse_args()
        attacker_user_id = args['attacker_user_id']
        attacked_user_id = args['attacked_user_id']
        weapon_types = json.loads(args['weapon_types'])
        if not self.validate_weapon_types(weapon_types):
            abort(400, 'Invalid weapon types')
        attacker = User.query.get_or_404(attacker_user_id)
        attacked = User.query.get_or_404(attacked_user_id)
        if not self.can_attack(attacker.army, weapon_types):
            abort(400, 'You do not have enough turns to attack')
        battle_result = attack(attacker.army, attacked.army, weapon_types)
        battle_result = BattleResult(attacker_army=attacker.army,
                                     attacked_army=attacked.army,
                                     attacker_result=battle_result.attacker_results,
                                     attacked_result=battle_result.attacked_results,
                                     did_attacker_win=battle_result.did_attacker_win)
        db.session.add(battle_result)
        db.session.commit()
        return {
            'is_winner': battle_result.did_attacker_win,
            'url': url_for('attack.battle_results', battle_result_id=battle_result.id)
        }


subpath_api.add_resource(AttackAPI, '/attack', endpoint='attack')
