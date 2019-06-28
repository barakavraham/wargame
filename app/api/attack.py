from app import db
from app.api import base_api, SubpathApi
from app.permissions.permissions import login_required_for_api
from flask_restful import Resource, reqparse
from flask import url_for, render_template
from app.models.user import User

subpath_api = SubpathApi(base_api, '/attack', 'attack')

class OpenProfileWindowAPI(Resource):
    def __init__(self):
        super(OpenProfileWindowAPI, self).__init__()

    def get(self, army_email):
        user = User.query.filter_by(email=army_email).first_or_404()
        html_profile = render_template('attack/profile.html', user=user)
        return html_profile

subpath_api.add_resource(OpenProfileWindowAPI, '/user_profile/<string:army_email>', endpoint='user_profile/<string:army_email>')
