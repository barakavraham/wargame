from app import SHOP_ITEMS
from app.permissions.permissions import army_name_required
from flask import render_template, Blueprint
from flask_login import login_required, current_user
from dataclasses import dataclass

shop = Blueprint('shop', __name__, template_folder='templates')


@dataclass
class UpgradePrice:
    coin: int
    metal: int
    wood: int
    picture_name: str


class UpgradableItem:
    def __init__(self, level_1: UpgradePrice, level_2: UpgradePrice, level_3: UpgradePrice, level_4: UpgradePrice, level_5: UpgradePrice):
        self.level_1 = level_1
        self.level_2 = level_2
        self.level_3 = level_3
        self.level_4 = level_4
        self.level_5 = level_5

    def get_user_level(self, upgrade):
        return current_user.army.upgrades.get_upgrade_level(upgrade)



class TechUpgrades:
    def __init__(self, ground_weapons: UpgradableItem, bombs: UpgradableItem, air_weapons: UpgradableItem, country: UpgradableItem):
        self.ground_weapons = ground_weapons
        self.bombs = bombs
        self.air_weapons = air_weapons
        self.country = country

    def get_to_level(self, upgrade):
        return getattr(self, upgrade)


TECH_UPGRADES = TechUpgrades(
    ground_weapons = UpgradableItem(
        level_1=UpgradePrice(200, 400, 600, "upgrade"),
        level_2=UpgradePrice(300, 700, 1000, "upgrade"),
        level_3=UpgradePrice(400, 900, 1600, "upgrade"),
        level_4=UpgradePrice(800, 2000, 2600, "upgrade"),
        level_5=UpgradePrice(2000, 4000, 5600, "upgrade")),
    bombs = UpgradableItem(
        level_1=UpgradePrice(200, 400, 600, "upgrade"),
        level_2=UpgradePrice(300, 700, 1000, "upgrade"),
        level_3=UpgradePrice(400, 900, 1600, "upgrade"),
        level_4=UpgradePrice(800, 2000, 2600, "upgrade"),
        level_5=UpgradePrice(2000, 4000, 5600, "upgrade")),
    air_weapons = UpgradableItem(
        level_1=UpgradePrice(200, 400, 600, "upgrade"),
        level_2=UpgradePrice(300, 700, 1000, "upgrade"),
        level_3=UpgradePrice(400, 900, 1600, "upgrade"),
        level_4=UpgradePrice(800, 2000, 2600, "upgrade"),
        level_5=UpgradePrice(2000, 4000, 5600, "upgrade")),
    country = UpgradableItem(
        level_1=UpgradePrice(200, 400, 600, "upgrade"),
        level_2=UpgradePrice(300, 700, 1000, "upgrade"),
        level_3=UpgradePrice(400, 900, 1600, "upgrade"),
        level_4=UpgradePrice(800, 2000, 2600, "upgrade"),
        level_5=UpgradePrice(2000, 4000, 5600, "upgrade")))

tech_upgrades_list = []
for upgrade in [a for a in dir(TECH_UPGRADES) if not a.startswith('__') and not callable(getattr(TECH_UPGRADES,a))]:
    tech_upgrades_list.append(upgrade)


@shop.route("/")
@login_required
@army_name_required
def index():
    return render_template('shop/index.html', shop_items=SHOP_ITEMS, tech_upgrades=TECH_UPGRADES, tech_upgrades_list=tech_upgrades_list)
