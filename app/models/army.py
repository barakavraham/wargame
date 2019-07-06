from app.models.user import User # DO NOT DELETE
from app import db
from sqlalchemy.orm import backref
from app.utils.shop import TECH_UPGRADES, SHOP_ITEMS
from sqlalchemy_utils.types import JSONType


class Army(db.Model):
    __tablename__ = 'armies'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    name = db.Column(db.String(20), unique=True)
    coin = db.Column(db.Integer, nullable=False, default=100)
    wood = db.Column(db.Integer, nullable=False, default=100)
    metal = db.Column(db.Integer, nullable=False, default=100)
    field = db.Column(db.Integer, nullable=False, default=1000)
    diamond = db.Column(db.Integer, nullable=False, default=0)
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

    @staticmethod
    def get_num_with_comma(num):
        return '{:,}'.format(num)

    def get_power(self, unit_type):
        total_power = 0
        for weapon in SHOP_ITEMS:
            if SHOP_ITEMS[weapon].weapon_type == unit_type:
                total_power += self.get_item_amount(weapon) * SHOP_ITEMS[weapon].power
        return total_power


class Upgrade(db.Model):
    __tablename__ = 'upgrades'

    id = db.Column(db.Integer, primary_key=True)
    army_id = db.Column(db.Integer, db.ForeignKey('armies.id'))
    ground_weapons = db.Column(db.Integer, nullable=False, default=0)
    bombs = db.Column(db.Integer, nullable=False, default=0)
    air_weapons = db.Column(db.Integer, nullable=False, default=0)
    country = db.Column(db.Integer, nullable=False, default=0)

    army = db.relationship('Army', backref=backref('upgrades', uselist=False))

    def get_current_level(self, upgrade_name):
        current_level = getattr(self, upgrade_name)
        return f'level_{current_level}'

    def get_next_level(self, upgrade_name):
        current_level = getattr(self, upgrade_name)
        return f'level_{current_level + 1}'

    def get_current_level_num(self, upgrade_name):
        return getattr(self, upgrade_name)

    def add_level(self, upgrade_name):
        current_level = self.get_current_level_num(upgrade_name)
        setattr(self, upgrade_name, current_level + 1)

    def is_max_level(self, upgrade_name):
        current_level = getattr(self, upgrade_name)
        return current_level == TECH_UPGRADES[upgrade_name].max_level


class BattleResult(db.Model):
    __tablename__ = 'battle_results'

    id = db.Column(db.Integer, primary_key=True)
    attacker_army_id = db.Column(db.Integer, db.ForeignKey('armies.id'))
    attacked_army_id = db.Column(db.Integer, db.ForeignKey('armies.id'))
    attacker_result = db.Column(JSONType, nullable=False)
    attacked_result = db.Column(JSONType, nullable=False)
    did_attacker_win = db.Column(db.Boolean)

    attacker_army = db.relationship('Army', foreign_keys=[attacker_army_id])
    attacked_army = db.relationship('Army', foreign_keys=[attacked_army_id])
