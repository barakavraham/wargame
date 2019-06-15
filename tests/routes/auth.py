from app import db, bcrypt
from app.models.user import User
from app.models.army import Army, Upgrade
from tests.utils import format_response
from tests.routes import RouteTestCase

class AuthRouteTestCase(RouteTestCase):

    def setUp(self):
        self.logout()

    def test_login_required(self):
        res = self.test_client.get('/attack', follow_redirects=True)
        self.assertIn('<a id="login-btn" class="nav-link" href="javascript: void(0);">Login</a>', format_response(res))
    
    def test_army_name_required(self):
        user = self.create_user('no.army@gmail.com', 'password', 'NoArmy')
        user.army.name = None
        db.session.commit()
        self.login(user.email, 'password')
        res = self.test_client.get('/attack', follow_redirects=True)
        self.assertIn('<p class="h4 mb-4">Choose army name</p>', format_response(res))

    def test_auth_login(self):
        res = self.test_client.post('/auth/login', data=dict())
        self.assertIn('<div class= "invalid-feedback mb-4"> This field is required. </div>', format_response(res))
        self.login()
        res = self.test_client.get('/')
        self.assertIn('<a class="nav-link" href="/auth/logout">Logout</a>', format_response(res))
        self.logout()

    def test_auth_register(self):
        res = self.test_client.post('/auth/register', data=dict())
        self.assertIn('<div class= "invalid-feedback"> This field is required. </div>', format_response(res))
        res = self.test_client.post('/auth/register', data=dict(email='TestEmail@test.com',
                                                                password='123456',
                                                                confirm_password='123456',
                                                                army_name='TestArmyName'), follow_redirects=True)
        self.assertIn('<a class="nav-link" href="/auth/logout">Logout</a>', format_response(res))
        user = User.query.filter_by(email='TestEmail@test.com').first()
        self.assertIsNotNone(user)
        self.assertIsNotNone(user.army)
        self.assertIsNotNone(user.army.upgrades)
    
    def test_auth_logout(self):
        self.login()
        res = self.test_client.get('/')
        self.assertIn('<a class="nav-link" href="/auth/logout">Logout</a>', format_response(res))
        res = self.logout()
        self.assertIn('<a id="login-btn" class="nav-link" href="javascript: void(0);">Login</a>', format_response(res))


