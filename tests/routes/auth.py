from app import db
from app.models.user import User
from app.models.army import Army
from tests.utils import format_response
from tests.routes import RouteTestCase


class AuthRoutesTestCase(RouteTestCase):

    def setUp(self):
        self.logout()

    def test_login_required(self):
        res = self.test_client.get('/attack', follow_redirects=True)
        self.assertIn('<a id="login-btn" class="nav-link" href="javascript: void(0);">Login</a>', format_response(res))
    
    def test_army_name(self):
        user = self.create_user('no.army@gmail.com', 'password', 'NoArmy')
        user.army.name = None
        db.session.commit()
        self.login(user.email, 'password')
        res = self.test_client.get('/attack', follow_redirects=True)
        self.assertIn('<p class="h4 mb-4">Choose army name</p>', format_response(res))
        res = self.test_client.post('/profile/set_army_name', data=dict(army_name='@LitArmy#'), follow_redirects=True)
        self.assertIn('<div class= "invalid-feedback"> Army name must contain only letters and numbers </div>',
                      format_response(res))
        army_name = db.session.query(Army).filter(Army.name.isnot(None)).first().name
        res = self.test_client.post('/profile/set_army_name', data=dict(army_name=army_name), follow_redirects=True)
        self.assertIn('<div class= "invalid-feedback"> This army name already exists </div>', format_response(res))
        self.test_client.post('/profile/set_army_name', data=dict(army_name='LitArmy'), follow_redirects=True)
        self.assertIsNotNone(user.army.name)
        # If we already have an army name, we should be redirected to 'base.index'
        res = self.test_client.get('profile/set_army_name', follow_redirects=True)
        self.assertIn('Search for resources', format_response(res))

    def test_auth_login(self):
        res = self.test_client.post('/auth/login', data=dict())
        self.assertIn('<div class= "invalid-feedback mb-4"> This field is required. </div>', format_response(res))
        user = self.create_user('email@gmail.com', 'password', 'armyting')
        self.test_client.post('/auth/login', data=dict(email=user.email, password='password', remember=True))
        res = self.test_client.get('/', follow_redirects=True)
        self.assertIn('<a class="nav-link" href="/auth/logout">Logout</a>', format_response(res))
        self.logout()

    def test_auth_register(self):
        res = self.test_client.post('/auth/register', data=dict())
        self.assertIn('<div class= "invalid-feedback"> This field is required. </div>', format_response(res))
        res = self.test_client.post('/auth/register', data=dict(email='TestEmail@test.com',
                                                                password='123456',
                                                                confirm_password='123456',
                                                                army_name=self.user.army.name), follow_redirects=True)
        self.assertIn('<div class= "invalid-feedback"> This army name is already taken </div>', format_response(res))
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
