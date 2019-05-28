from flask_login import current_user
from typing import List


class ShopItem:
    def __init__(self, prices=List[tuple], power: int = 0, picture_name: str = 'default', display_name: str = ''):
        self.prices = dict(prices)
        self.power = power
        self.picture_name = picture_name
        self.display_name = display_name

    def price(self, amount=1):
        return {item: self.prices[item] * amount for item in self.prices}


class UpgradableItem:
    def __init__(self, level_1: ShopItem, level_2: ShopItem, level_3: ShopItem, level_4: ShopItem, level_5: ShopItem):
        self.level_1 = level_1
        self.level_2 = level_2
        self.level_3 = level_3
        self.level_4 = level_4
        self.level_5 = level_5

    @staticmethod
    def get_item_level(upgrade):
        return current_user.army.upgrades.get_upgrade_level(upgrade)

    def __getitem__(self, level):
        if isinstance(level, str):
            return getattr(self, level, None)
        return getattr(self, f'level_{level}', None)

    def __iter__(self):
        return iter(self.__dict__)


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
        picture_name='pistol',
        display_name='Pistol'
    ),
    'rifle': ShopItem(
        prices=[('coin', 400), ('metal', 150)],
        power=2_500,
        picture_name='rifle',
        display_name='Rifle'
    ),
    'tank': ShopItem(
        prices=[('coin', 800), ('metal', 330)],
        power=6_000,
        picture_name='tank',
        display_name='Tank'
    ),
    'missile_1': ShopItem(
        prices=[('coin', 1_600), ('metal', 700)],
        power=12_000,
        picture_name='missile_1',
        display_name='Missile Type A'
    ),
    'missile_2': ShopItem(
        prices=[('coin', 4_000), ('metal', 1_800)],
        power=25_000,
        picture_name='missile_2',
        display_name='Missile Type B'
    ),
    'missile_3': ShopItem(
        prices=[('coin', 10_600), ('metal', 3_700)],
        power=50_000,
        picture_name='missile_3',
        display_name='Missile Type C'
    ),
    'jet': ShopItem(
        prices=[('coin', 35_000), ('metal', 12_000)],
        power=150_000,
        picture_name='jet',
        display_name='Jet'
    ),
}


TECH_UPGRADES = TechUpgrades(
    ground_weapons=UpgradableItem(
        level_1=ShopItem([('coin', 200), ('metal', 400), ('wood', 600)], picture_name="upgrade"),
        level_2=ShopItem([('coin', 300), ('metal', 700), ('wood', 1_000)], picture_name="upgrade"),
        level_3=ShopItem([('coin', 400), ('metal', 900), ('wood', 1_600)], picture_name="upgrade2"),
        level_4=ShopItem([('coin', 800), ('metal', 2_000), ('wood', 2_600)], picture_name="upgrade"),
        level_5=ShopItem([('coin', 2_000), ('metal', 4_000), ('wood', 5_600)], picture_name="upgrade")),
    bombs=UpgradableItem(
        level_1=ShopItem([('coin', 200), ('metal', 400), ('wood', 600)], picture_name="upgrade"),
        level_2=ShopItem([('coin', 300), ('metal', 700), ('wood', 1_000)], picture_name="upgrade"),
        level_3=ShopItem([('coin', 400), ('metal', 900), ('wood', 1_600)], picture_name="upgrade2"),
        level_4=ShopItem([('coin', 800), ('metal', 2_000), ('wood', 2_600)], picture_name="upgrade"),
        level_5=ShopItem([('coin', 2_000), ('metal', 4_000), ('wood', 5_600)], picture_name="upgrade")),
    air_weapons=UpgradableItem(
        level_1=ShopItem([('coin', 200), ('metal', 400), ('wood', 600)], picture_name="upgrade"),
        level_2=ShopItem([('coin', 300), ('metal', 700), ('wood', 1_000)], picture_name="upgrade"),
        level_3=ShopItem([('coin', 400), ('metal', 900), ('wood', 1_600)], picture_name="upgrade2"),
        level_4=ShopItem([('coin', 800), ('metal', 2_000), ('wood', 2_600)], picture_name="upgrade"),
        level_5=ShopItem([('coin', 2_000), ('metal', 4_000), ('wood', 5_600)], picture_name="upgrade")),
    country=UpgradableItem(
        level_1=ShopItem([('coin', 200), ('metal', 400), ('wood', 600)], picture_name="upgrade"),
        level_2=ShopItem([('coin', 300), ('metal', 700)], picture_name="upgrade"),
        level_3=ShopItem([('coin', 400)], picture_name="upgrade2"),
        level_4=ShopItem([('coin', 800), ('metal', 2_000), ('wood', 2_600)], picture_name="upgrade"),
        level_5=ShopItem([('coin', 2_000), ('metal', 4_000), ('wood', 5_600)], picture_name="upgrade")))


def can_afford(prices):
    for resource in prices:
        if getattr(current_user.army, resource) <= prices[resource]:
            return False
    return True
