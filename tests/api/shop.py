from app import db
from app.utils.shop import TECH_UPGRADES
from tests.api import APITestCase


class ShopAPITestCase(APITestCase):
    
    def setUp(self):
        self.login()
        self.give_resources()

    def tearDown(self):
        self.reset_resources()
        self.logout()

    def test_buy_resources(self):
        url = '/api/shop/buy_resources'
        res = self.test_client.post(url, json={'amount': -2, 'item': 'pistol'})
        self.assertEqual(res.status_code, 400)
        res = self.test_client.post(url, json={'amount': 10, 'item': 'pistol'})
        self.assertEqual(res.status_code, 200)
        user = self.get_user()
        self.assertEqual(user.army.pistol, 10)
        res = self.test_client.post(url, json={'amount': 1, 'item': 'no_name_test'})
        self.assertEqual(res.status_code, 400)
        res = self.test_client.post(url, json={'amount': 999999, 'item': 'jet'})
        self.assertEqual(res.status_code, 400)

    def test_upgrade(self):
        url = '/api/shop/upgrade'
        self.reset_resources()
        res = self.test_client.post(url, json={'upgrade': 'ground_weapons', 'level': 1})
        self.assertEqual(res.status_code, 400)
        res = self.test_client.post(url, json={'upgrade': 'no_name_test', 'level': 1})
        self.give_resources()
        self.assertEqual(res.status_code, 400)
        res = self.test_client.post(url, json={'upgrade': 'ground_weapons', 'level': 1})
        self.assertEqual(res.status_code, 200)
        user = self.get_user()
        self.assertEqual(user.army.upgrades.ground_weapons, 1)
        res = self.test_client.post(url, json={'upgrade': 'ground_weapons', 'level': 3})
        self.assertEqual(res.status_code, 400)
        user = self.get_user()
        self.assertEqual(user.army.upgrades.ground_weapons, 1)
        user.army.upgrades.ground_weapons = TECH_UPGRADES.ground_weapons.max_level
        db.session.commit()
        res = self.test_client.post(url, json={'upgrade': 'ground_weapons', 
                                               'level': TECH_UPGRADES.ground_weapons.max_level + 1})
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json, {'max_level': True})
