from flask_login import current_user
from typing import List


class ShopItem:
    def __init__(self,
                 prices: List[tuple],
                 power: int = 0,
                 picture_name: str = 'upgrade',
                 display_name: str = '',
                 weapon_type: str = ''):
        self.prices = dict(prices)
        self.power = power
        self.picture_name = picture_name
        self.display_name = display_name
        self.weapon_type = weapon_type

    def price(self, amount=1):
        return {item: self.prices[item] * amount for item in self.prices}


class UpgradableItem:
    def __init__(self,
                level_1: ShopItem = None, level_2: ShopItem = None,
                level_3: ShopItem = None, level_4: ShopItem = None,
                level_5: ShopItem = None, level_6: ShopItem = None,
                level_7: ShopItem = None, level_8: ShopItem = None,
                level_9: ShopItem = None, max_level: int = None):

        self.level_1 = level_1
        self.level_2 = level_2
        self.level_3 = level_3
        self.level_4 = level_4
        self.level_5 = level_5
        self.level_6 = level_6
        self.level_7 = level_7
        self.level_8 = level_8
        self.level_9 = level_9
        self.max_level = max_level

    @staticmethod
    def get_item_level(upgrade):
        return current_user.army.upgrades.get_upgrade_level(upgrade)

    def __getitem__(self, level):
        if isinstance(level, str):
            return getattr(self, level, None)
        return getattr(self, f'level_{level}', None)

    def __iter__(self):
        return iter(self.__dict__)

    def get_max_level_picture(self):
        return self[self.max_level].picture_name


class TechUpgrades:
    def __init__(self, ground_weapons: UpgradableItem, bombs: UpgradableItem, air_weapons: UpgradableItem, country: UpgradableItem):
        self.ground_weapons = ground_weapons
        self.bombs = bombs
        self.air_weapons = air_weapons
        self.country = country

    def __getitem__(self, upgrade_name):
        return getattr(self, upgrade_name)

    def __iter__(self):
        return iter(self.__dict__)


SHOP_ITEMS = {
    'pistol': ShopItem(
        prices=[('coin', 200), ('metal', 50)],
        power=1_000,
        picture_name='pistol.png',
        display_name='Pistols',
        weapon_type='ground_weapons'
    ),
    'rifle': ShopItem(
        prices=[('coin', 400), ('metal', 150)],
        power=2_500,
        picture_name='rifle.png',
        display_name='Rifles',
        weapon_type='ground_weapons'
    ),
    'tank': ShopItem(
        prices=[('coin', 800), ('metal', 330)],
        power=6_000,
        picture_name='tank.png',
        display_name='Tanks',
        weapon_type='ground_weapons'
    ),
    'missile_1': ShopItem(
        prices=[('coin', 1_600), ('metal', 700)],
        power=12_000,
        picture_name='missile_1.png',
        display_name='Missiles Type A',
        weapon_type='bombs'
    ),
    'missile_2': ShopItem(
        prices=[('coin', 4_000), ('metal', 1_800)],
        power=25_000,
        picture_name='missile_2.png',
        display_name='Missiles Type B',
        weapon_type='bombs'
    ),
    'missile_3': ShopItem(
        prices=[('coin', 10_600), ('metal', 3_700)],
        power=50_000,
        picture_name='missile_3.png',
        display_name='Missiles Type C',
        weapon_type='bombs'
    ),
    'jet': ShopItem(
        prices=[('coin', 35_000), ('metal', 12_000)],
        power=150_000,
        picture_name='jet.png',
        display_name='Jets',
        weapon_type='air_weapons'
    ),
}


TECH_UPGRADES = TechUpgrades(
    ground_weapons=UpgradableItem(
        level_1=ShopItem([('coin', 200), ('metal', 400), ('wood', 600)], picture_name="upgrade.png"),
        level_2=ShopItem([('coin', 300), ('metal', 700), ('wood', 1_000)], picture_name="upgrade.png"),
        level_3=ShopItem([('coin', 400), ('metal', 900), ('wood', 1_600)], picture_name="upgrade.png"),
        level_4=ShopItem([('coin', 800), ('metal', 2_000), ('wood', 2_600)], picture_name="upgrade2.png"),
        max_level=4),
    bombs=UpgradableItem(
        level_1=ShopItem([('coin', 200), ('metal', 400), ('wood', 600)], picture_name="upgrade.png"),
        level_2=ShopItem([('coin', 300), ('metal', 700), ('wood', 1_000)], picture_name="upgrade.png"),
        level_3=ShopItem([('coin', 400), ('metal', 900), ('wood', 1_600)], picture_name="upgrade2.png"),
        level_4=ShopItem([('coin', 800), ('metal', 2_000), ('wood', 2_600)], picture_name="upgrade.png"),
        level_5=ShopItem([('coin', 2_000), ('metal', 4_000), ('wood', 5_600)], picture_name="upgrade.png"),
        max_level=5),
    air_weapons=UpgradableItem(
        level_1=ShopItem([('coin', 200), ('metal', 400), ('wood', 600)], picture_name="upgrade.png"),
        level_2=ShopItem([('coin', 300), ('metal', 700), ('wood', 1_000)], picture_name="upgrade.png"),
        level_3=ShopItem([('coin', 400), ('metal', 900), ('wood', 1_600)], picture_name="upgrade2.png"),
        level_4=ShopItem([('coin', 800), ('metal', 2_000), ('wood', 2_600)], picture_name="upgrade.png"),
        level_5=ShopItem([('coin', 2_000), ('metal', 4_000), ('wood', 5_600)], picture_name="upgrade.png"),
        max_level=5),
    country=UpgradableItem(
        level_1=ShopItem([('coin', 200), ('metal', 400), ('wood', 600)], picture_name="upgrade.png"),
        level_2=ShopItem([('coin', 300), ('metal', 700)], picture_name="upgrade.png"),
        level_3=ShopItem([('coin', 400)], picture_name="upgrade2.png"),
        level_4=ShopItem([('coin', 800), ('metal', 2_000), ('wood', 2_600)], picture_name="upgrade.png"),
        max_level=4))
        
        


def can_afford(prices):
    for resource in prices:
        if getattr(current_user.army, resource) <= prices[resource]:
            return False
    return True
