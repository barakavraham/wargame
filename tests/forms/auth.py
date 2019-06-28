from app import db
from flask import url_for
from tests.utils import format_response
from tests.forms import FormTestCase
from app.forms.auth import RegistrationForm


class AuthFormTestCase(FormTestCase):

    def test_registration_form(self):
        res = RegistrationForm(data={
                            'email': 'testEmail@gmail.com',
                            'password': '456123',
                            'confirm_password': '456123',
                            'army_name': 'testName'})
        self.assertEqual(res.validate_on_submit(), True)
