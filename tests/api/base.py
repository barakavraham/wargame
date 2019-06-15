from app import db
from tests.utils import format_response
from tests.api import APITestCase


class BaseAPITestCase(APITestCase):
    
    def setUp(self):
        self.login()
        self.get_user().army.turns = 200
        self.give_resources()

    def tearDown(self):
        self.reset_resources()
        self.logout()
    
    def test_search_resources(self):
        url = '/api/base/search_resources'
        res = self.test_client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertIn('turns', res.json)
        self.get_user().army.turns = 0
        db.session.commit()
        res = self.test_client.get(url)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json, {'turns': 0, 'added_resources': None})
    
    def test_search_fields(self):
        url = '/api/base/search_field'
        res = self.test_client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertIn('turns', res.json)
        self.get_user().army.turns = 0
        db.session.commit()
        res = self.test_client.get(url)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json, {'turns': 0, 'added_resources': None})