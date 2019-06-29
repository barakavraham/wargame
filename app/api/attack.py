from flask import render_template, abort
from flask_restful import Resource, reqparse
from app.models.user import User
from app.api import base_api, SubpathApi
from app.permissions.permissions import login_required_for_api
from app.utils.attack import attack

subpath_api = SubpathApi(base_api, '/attack', 'attack')


class OpenProfileWindowAPI(Resource):
    decorators = [login_required_for_api]

    @staticmethod
    def get(army_email):
        user = User.query.filter_by(email=army_email).first_or_404()
        html_profile = render_template('attack/profile.html', user=user)
        return html_profile


subpath_api.add_resource(OpenProfileWindowAPI,
                         '/user_profile/<string:army_email>',
                         endpoint='user_profile/<string:army_email>')


class AttackAPI(Resource):
    decorators = [login_required_for_api]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('attacker_user_id', type=int, required=False)
        self.reqparse.add_argument('attacked_user_id', type=int, required=False)
        super(AttackAPI, self).__init__()

    def post(self):
        args = self.reqparse.parse_args()
        attacker_user_id = args['attacker_user_id']
        attacked_user_id = args['attacked_user_id']
        attacker = User.query.get_or_404(attacker_user_id)
        attacked = User.query.get_or_404(attacked_user_id)
        battle_results = attack(attacker.army, attacked.army, ['ground_weapons'])
        return {
            'attacker_results': battle_results.attacker_results,
            'attacked_results': battle_results.attacked_results,
            'is_winner': battle_results.is_winner
        }


subpath_api.add_resource(AttackAPI, '/attack', endpoint='attack')
