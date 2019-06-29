from math import ceil
from random import randint, uniform
from app import db
from app.api import base_api, SubpathApi
from app.permissions.permissions import login_required_for_api
from flask_restful import Resource
from flask_login import current_user
from flask import url_for

subpath_api = SubpathApi(base_api, '/base', 'base')


class SearchResourcesAPI(Resource):
    decorators = [login_required_for_api]

    def __init__(self):
        super(SearchResourcesAPI, self).__init__()

    @staticmethod
    def search_for_resources():
        random_percentage = uniform(5.0, 10.0)
        found_resource = ceil(current_user.army.field / random_percentage)
        return found_resource

    def search_for_diamonds(self, diamonds=0):
        random_num = randint(1, 2)
        return self.search_for_diamonds(diamonds + 1) + 1 if random_num == 1 and diamonds != 9 else 0

    @staticmethod
    def can_search():
        return current_user.army.turns >= 10

    def add_user_resources(self):
        added_resource = {
            'wood': {
                'amount': self.search_for_resources(),
                'picture': url_for('static', filename='images/wood.png')
            },
            'metal': {
                'amount': self.search_for_resources(),
                'picture': url_for('static', filename='images/metal.png')
            },
            'coin': {
                'amount': self.search_for_resources(),
                'picture': url_for('static', filename='images/coin.png')
            },
            'diamond': {
                'amount': self.search_for_diamonds(),
                'picture': url_for('static', filename='images/diamond.png')
            }
        }
        for resource in added_resource:
            current_user.army.add_item_amount(resource, added_resource[resource]['amount'])
        current_user.army.turns -= 10
        db.session.commit()

        return added_resource

    def get(self):
        added_resources = None
        can_search = self.can_search()
        if can_search:
            added_resources = self.add_user_resources()
        return {
            'turns': current_user.army.turns,
            'added_resources': added_resources
        }, 200 if can_search else 400


subpath_api.add_resource(SearchResourcesAPI, '/search_resources', endpoint='search_resources')


class SearchFieldAPI(Resource):
    decorators = [login_required_for_api]

    def __init__(self):
        super(SearchFieldAPI, self).__init__()

    @staticmethod
    def can_search():
        return current_user.army.turns >= 15

    @staticmethod
    def search_for_resources():
        random_field = randint(50, 100)
        return random_field

    def add_user_resources(self):
        added_resource = {
            'field': {
                'amount': self.search_for_resources(),
                'picture': url_for('static', filename='images/field.png')
            }
        }

        for resource in added_resource:
            current_user.army.add_item_amount(resource, added_resource[resource]['amount'])
        current_user.army.turns -= 15
        db.session.commit()

        return added_resource

    def get(self):
        can_search = self.can_search()
        added_resources = None
        if can_search:
            added_resources = self.add_user_resources()
        return {
           'turns': current_user.army.turns,
           'added_resources': added_resources
        }, 200 if can_search else 400


subpath_api.add_resource(SearchFieldAPI, '/search_field', endpoint='search_field')
