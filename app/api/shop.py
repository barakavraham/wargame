from app import db
from app.api import base_api, SubpathApi
from app.utils.shop import can_afford, SHOP_ITEMS, TECH_UPGRADES
from flask_restful import Resource, reqparse
from flask_login import current_user

subpath_api = SubpathApi(base_api, '/shop', 'shop')


class BuyResourcesAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('item', type=str, required=True, location='json')
        self.reqparse.add_argument('amount', type=int, required=True, location='json')
        super(BuyResourcesAPI, self).__init__()

    @staticmethod
    def can_buy(item, amount):
        prices = SHOP_ITEMS[item].price(amount)
        return can_afford(prices)

    def buy_item(self, item, amount):
        if not self.can_buy(item, amount):
            return False
        prices = SHOP_ITEMS[item].price(amount)
        for resource in prices:
            setattr(current_user.army, resource, getattr(current_user.army, resource) - prices[resource])
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

    @staticmethod
    def can_upgrade(upgrade, level):
        prices = TECH_UPGRADES[upgrade][level].prices
        return can_afford(prices)

    @staticmethod
    def is_max_level(upgrade, level):
        if TECH_UPGRADES[upgrade][level] is None:
            return True
        return False

    def upgrade(self, upgrade, level):
        if not self.can_upgrade(upgrade, level):
            return False
        prices = TECH_UPGRADES[upgrade][level].prices
        for resource in prices:
            setattr(current_user.army, resource, getattr(current_user.army, resource) - prices[resource])
        current_user.army.upgrades.add_level(upgrade)
        db.session.commit()
        return True

    def post(self):
        args = self.reqparse.parse_args()
        upgrade_name = args['upgrade']
        level = args['level']
        if self.is_max_level(upgrade_name, level):
            return {'max_level': True}, 400
        is_successful = self.upgrade(upgrade_name, level)
        upgrade = TECH_UPGRADES[upgrade_name][level + 1]
        prices = {
            resource: upgrade.prices[resource] for resource in upgrade.prices
        } if upgrade else None
        return {
                   'success': is_successful,
                   'prices': prices,
                   'max_level': self.is_max_level(upgrade_name, level + 1)
               }, 200 if is_successful else 400

    
subpath_api.add_resource(UpgradeAPI, '/upgrade', endpoint='upgrade')