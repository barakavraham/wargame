from tests.utils import format_response
from tests.routes import RouteTestCase

class BaseRouteTestCase(RouteTestCase):

    def setUp(self):
        self.login()
    
    def tearDown(self):
        self.logout()

    def test_base_index(self):
        res = self.test_client.get('/base', follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn('Search for your resources with low chance to find diamonds', format_response(res))
