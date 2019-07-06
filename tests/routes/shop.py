from tests.utils import format_response
from tests.routes import RouteTestCase


class ShopRouteTestCase(RouteTestCase):

    def setUp(self):
        self.login()
    
    def tearDown(self):
        self.logout()

    def test_shop_index(self):
        res = self.test_client.get('/shop', follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn('<div id="user-resources"', format_response(res))
        self.assertIn('<img class="power-img" src="/static/images/power.png" alt="power"/>', format_response(res))
