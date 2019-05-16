from app.models.user import User
from app import db
from flask_login import UserMixin
from sqlalchemy.orm import backref


class Army(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    name = db.Column(db.String(20), unique=False, nullable=False, default='NoName')
    gold = db.Column(db.Integer, nullable=False, default=100)
    wood = db.Column(db.Integer, nullable=False, default=100)
    metal = db.Column(db.Integer, nullable=False, default=100)
    field = db.Column(db.Integer, nullable=False, default=1000)
    power = db.Column(db.Integer, nullable=False, default=0)
    pistol = db.Column(db.Integer, nullable=False, default=0)
    rifle = db.Column(db.Integer, nullable=False, default=0)
    tank = db.Column(db.Integer, nullable=False, default=0)
    missile_1 = db.Column(db.Integer, nullable=False, default=0)
    missile_2 = db.Column(db.Integer, nullable=False, default=0)
    missile_3 = db.Column(db.Integer, nullable=False, default=0)
    jet = db.Column(db.Integer, nullable=False, default=0)
    clan = db.Column(db.String(15), default=None)
    turns = db.Column(db.Integer, nullable=False, server_default='60')
    

    user = db.relationship("User", backref=backref("army", uselist=False))

    def __repr__(self):
        return f'<Army {self.name}>'

    def get_item_amount(self, item):
        return getattr(self, item)

    def add_item_amount(self, item, amount):
        current_amount = self.get_item_amount(item)
        setattr(self, item, current_amount + amount)