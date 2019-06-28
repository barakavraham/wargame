import os
from unittest import TestCase
from app.models.user import User
from app.models.army import Army
from app import create_app, db
from app.utils.db import create_tables
from app.utils.user import create_user
from flask_login import login_user

TEST_USER_EMAIL = 'test@webgame.com'
TEST_USER_PASSWORD = 'password'
TEST_USER_ARMY_NAME = 'TestArmy'

class FormTestCase(TestCase):
    @classmethod
    def _remove_sqlite_test_db(cls):
        try:
            os.remove(cls.app.config['SQLALCHEMY_DATABASE_FILE'])
        except OSError:
            pass
    
    @classmethod
    def setupClass(cls):
        super(FormTestCase, cls).setUpClass()
        cls.app = create_app('testing')
        cls.test_client = cls.app.test_client()
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        cls._remove_sqlite_test_db()
        create_tables(db)
        cls.user = cls.create_user(email=TEST_USER_EMAIL, password=TEST_USER_PASSWORD, army_name=TEST_USER_ARMY_NAME)
        cls.user_id = cls.user.id

    @classmethod
    def tearDownClass(cls):
        cls.app_context.pop()
        cls._remove_sqlite_test_db()
        super(FormTestCase, cls).tearDownClass()

    @classmethod
    def create_user(cls, email=TEST_USER_EMAIL, password=TEST_USER_PASSWORD, army_name=TEST_USER_ARMY_NAME):
        return create_user(email, password, army_name)

    @classmethod
    def login(cls, email=TEST_USER_EMAIL, password=TEST_USER_PASSWORD, remember=False):
        return cls.test_client.post('/auth/login',
                                    data=dict(email=email,
                                              password=password,
                                              remember=remember),
                                              follow_redirects=True)

    def logout(self):
        return self.test_client.get('/auth/logout', follow_redirects=True)
