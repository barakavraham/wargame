from app.models.user import User # DO NOT DELETE
from app import db
from flask_login import UserMixin
from sqlalchemy.orm import backref


class Army(db.Model):
    __tablename__ = 'armies'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    name = db.Column(db.String(20), unique=True)
    coin = db.Column(db.Integer, nullable=False, default=100)
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
    turns = db.Column(db.Integer, nullable=False, default=60)

    user = db.relationship('User', backref=backref('army', uselist=False))

    def __repr__(self):
        return f'<Army {self.name}>'

    def get_item_amount(self, item):
        return getattr(self, item)

    def add_item_amount(self, item, amount):
        current_amount = self.get_item_amount(item)
        setattr(self, item, current_amount + amount)


class Upgrade(db.Model):
    __tablename__ = 'upgrades'

    id = db.Column(db.Integer, primary_key=True)
    army_id = db.Column(db.Integer, db.ForeignKey('armies.id'))
    ground_weapons = db.Column(db.Integer, nullable=False, default=1)
    bombs = db.Column(db.Integer, nullable=False, default=1)
    air_weapons = db.Column(db.Integer, nullable=False, default=1)
    country = db.Column(db.Integer, nullable=False, default=1)

    army = db.relationship('Army', backref=backref('upgrades', uselist=False))

    def get_upgrade_level(self, upgrade_name):
        upgrade_level = getattr(self, upgrade_name)
        return "level_"+str(upgrade_level)

    def get_upgrade_level_num(self, upgrade_name):
        return getattr(self, upgrade_name)
