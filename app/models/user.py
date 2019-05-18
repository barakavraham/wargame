import math
from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=True)
    avatar = db.Column(db.String(100), nullable=False, default='default.jpg')
    is_google_user = db.Column(db.Boolean, nullable=False, default='0')

    def get_gift(self):
        print(datetime.utcnow())
        self.army.gold += math.ceil(self.army.field / 10)
        self.army.metal += math.ceil(self.army.field / 20)
        self.army.wood += math.ceil(self.army.field / 20)
        self.army.turns += 3

    def __repr__(self):
        return f'<User {self.email}>'
