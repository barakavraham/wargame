from app import db, login_manager
from flask_login import UserMixin
from sqlalchemy.orm import backref

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=True)
    avatar = db.Column(db.String(100), nullable=False, default='default.jpg')
    is_google_user = db.Column(db.Boolean, nullable=False, default=False)



    def __repr__(self):
        return f'<User {self.email}>'


class Army(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    army_name = db.Column(db.String(20), unique=False, nullable=True)
    gold = db.Column(db.Integer, nullable=False, default=100)
    wood = db.Column(db.Integer, nullable=False, default=100)
    metal = db.Column(db.Integer, nullable=False, default=100)
    field = db.Column(db.Integer, nullable=False, default=1000)
    power = db.Column(db.Integer, nullable=False, default=100)
    soldiers = db.Column(db.Integer, nullable=False, default=0)
    tanks = db.Column(db.Integer, nullable=False, default=0)
    bombs = db.Column(db.Integer, nullable=False, default=0)

    user = db.relationship("User", backref=backref("army", uselist=False))

    def __repr__(self):
        return f'<Army {self.army_name}>'

