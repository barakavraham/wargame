from app import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    army_name = db.Column(db.String(24), nullable=True)
    password = db.Column(db.String(60), nullable=True)
    avatar = db.Column(db.String(100), nullable=False, default='default.jpg')
    is_google_user = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f'<User {self.email}>'
