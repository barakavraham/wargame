import math
from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime
from flask import url_for


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=True)
    avatar = db.Column(db.String(200), nullable=False, default='default.png')
    is_google_user = db.Column(db.Boolean, nullable=False, default=False)

    def get_gift(self):
        print(f'{datetime.utcnow()} - {repr(self)}')
        self.army.coin += math.ceil(self.army.field / 10)
        self.army.metal += math.ceil(self.army.field / 20)
        self.army.wood += math.ceil(self.army.field / 20)
        self.army.turns += 3

    def __repr__(self):
        return f'<User {self.email}>'

class Mail(db.Model):
    __tablename__ = 'mails'

    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    title = db.Column(db.String(16))
    content = db.Column(db.String(256))
    did_viewed = db.Column(db.Boolean, nullable=False, default=False)
    timestamp = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)

    author_user = db.relationship('User', foreign_keys=[author_id])
    recipient_user = db.relationship('User', foreign_keys=[recipient_id])
