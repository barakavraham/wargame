from app import db
from app.api import base_api, SubpathApi
from flask_restful import Resource, reqparse
from flask_login import current_user
from flask import url_for
import random, math

subpath_api = SubpathApi(base_api, '/base', 'base')


class SearchResourcesAPI(Resource):

    def __init__(self):
        super(SearchResourcesAPI, self).__init__()

    def search_for_resources(self):
        randomPercentage = random.uniform(5.0,10.0)
        resourceFound = math.ceil(current_user.army.field/randomPercentage)
        return resourceFound

    def search_for_diamond(self):
        randomNum = random.randint(0,10)
        if randomNum == 1:
            return 1
        else:
            return 0

    def can_search(self):
        return current_user.army.turns >= 10

    def add_user_resources(self):
        add_resource = {
            'wood': {
                'amount': self.search_for_resources(),
                'picture': url_for ('static', filename=f'images/wood.png')
            },
            'metal': {
                'amount': self.search_for_resources(),
                'picture': url_for ('static', filename=f'images/metal.png')
            },
            'coin': {
                'amount': self.search_for_resources(),
                'picture': url_for ('static', filename=f'images/coin.png')
            },
            'diamond': {
                'amount': self.search_for_diamond(),
                'picture': url_for ('static', filename=f'images/diamond.png')
            }
        }
        for resource in add_resource:
            current_user.army.add_item_amount(resource, add_resource[resource]['amount'])
        current_user.army.turns -= 10
        db.session.commit()

        return add_resource


    def get(self):
        is_successful = self.can_search() 
        if self.can_search():      
            add_resource = self.add_user_resources()
        return {
            'turns': current_user.army.turns, 
            'added_resource': add_resource
            }, 200 if is_successful else 400

subpath_api.add_resource(SearchResourcesAPI, '/search_resources', endpoint='search_resources')


class searchFieldAPI(Resource):

    def __init__(self):
        super(searchFieldAPI, self).__init__()

    def can_search(self):
        return current_user.army.turns >= 15

    def search_for_resources(self):
        random_field = random.randint(50,100)
        return random_field

    def add_user_resources(self):
        add_resource = {
            'field': {'amount': self.search_for_resources(), 'picture': url_for ('static', filename=f'images/field.png') }
        }

        for resource in add_resource:
            current_user.army.add_item_amount(resource, add_resource[resource]['amount'])
        current_user.army.turns -= 15
        db.session.commit()

        return add_resource

    def get(self):
        is_successful = self.can_search()
        if self.can_search():
            add_resource = self.add_user_resources()
        return {
            'turns': current_user.army.turns, 
            'added_resource': add_resource
            }, 200 if is_successful else 400

subpath_api.add_resource(searchFieldAPI, '/search_field', endpoint='search_field')