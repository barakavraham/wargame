from app import db
from app.api import base_api, SubpathApi
from app.utils.shop import SHOP_ITEMS, TECH_UPGRADES
from flask_restful import Resource, reqparse
from flask_login import current_user

subpath_api = SubpathApi(base_api, '/shop', 'shop')


class BuyResourcesAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('item', type=str, required=True, location='json')
        self.reqparse.add_argument('amount', type=int, required=True, location='json')
        super(BuyResourcesAPI, self).__init__()

    def can_buy(self, item, amount):
        prices = SHOP_ITEMS[item].price(amount)
        return current_user.army.coin >= prices.coin and current_user.army.metal >= prices.metal


    def buy_item(self, item, amount):
        if not self.can_buy(item, amount):
            return False
        prices = SHOP_ITEMS[item].price(amount)
        current_user.army.coin -= prices.coin
        current_user.army.metal -= prices.metal
        current_user.army.add_item_amount(item, amount)
        db.session.commit()
        return True

    def post(self):
        args = self.reqparse.parse_args()
        if args['amount'] <= 0:
            return {'success': False}
        is_successful = self.buy_item(args['item'], args['amount'])
        return {'success': is_successful}, 200 if is_successful else 400


subpath_api.add_resource(BuyResourcesAPI, '/buy_resources', endpoint='buy_resources')


class UpgradeAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('upgrade', type=str, required=True, location='json')
        self.reqparse.add_argument('level', type=int, required=True, location='json')
        super(UpgradeAPI, self).__init__()

    def can_upgrade(self, upgrade, level):
        prices = TECH_UPGRADES.__dict__[upgrade].__dict__[f'level_{level}']
        return (current_user.army.coin >= prices.coin and
                current_user.army.metal >= prices.metal and
                current_user.army.wood >= prices.wood)


    def upgrade(self, upgrade, level):
        if not self.can_upgrade(upgrade, level):
            return False
        prices = TECH_UPGRADES.__dict__[upgrade].__dict__[f'level_{level}']
        current_user.army.coin -= prices.coin
        current_user.army.metal -= prices.metal
        current_user.army.wood -= prices.wood
        current_user.army.upgrades.add_level(upgrade)
        db.session.commit()
        return True #test

    def post(self):
        args = self.reqparse.parse_args()
        is_successful = self.upgrade(args['upgrade'], args['level'])
        return {'success': is_successful}, 200 if is_successful else 400

    
subpath_api.add_resource(UpgradeAPI, '/upgrade', endpoint='upgrade')