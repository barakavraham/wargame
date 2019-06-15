from tests.utils import format_response
from tests.routes import RouteTestCase

class AttackRouteTestCase(RouteTestCase):

    def setUp(self):
        self.login()
    
    def tearDown(self):
        self.logout()

    def test_attack_index(self):
        res = self.test_client.get('/attack', follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn('<th scope="col">Rank</th>', format_response(res))

        res = self.test_client.get('/attack/1', follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn('<th scope="col">Rank</th>', format_response(res))
