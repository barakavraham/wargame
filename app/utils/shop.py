from flask_login import current_user
from dataclasses import dataclass


@dataclass
class ItemPrice:
    coin: int
    metal: int


@dataclass
class UpgradePrice:
    coin: int
    metal: int
    wood: int
    picture_name: str


class ShopItem:
    def __init__(self, coin: int, metal: int, power: int, picture_name: str):
        self.coin = coin
        self.metal = metal
        self.power = power
        self.picture_name = picture_name

    def price(self, amount):
        return ItemPrice(self.coin * amount, self.metal * amount)


SHOP_ITEMS = {
    'pistol': ShopItem(200, 50, 1_000, 'pistol'),
    'rifle': ShopItem(400, 150, 2_500, 'rifle'),
    'tank': ShopItem(800, 330, 6_000, 'tank'),
    'missile_1': ShopItem(1_600, 700, 12_000, 'missile_1'),
    'missile_2': ShopItem(4_000, 1_800, 25_000, 'missile_2'),
    'missile_3': ShopItem(10_600, 3_700, 50_000, 'missile_3'),
    'jet': ShopItem(35_000, 12_000, 150_000, 'jet'),
}


class UpgradableItem:
    def __init__(self, level_1: UpgradePrice, level_2: UpgradePrice, level_3: UpgradePrice, level_4: UpgradePrice, level_5: UpgradePrice):
        self.level_1 = level_1
        self.level_2 = level_2
        self.level_3 = level_3
        self.level_4 = level_4
        self.level_5 = level_5

    @staticmethod
    def get_item_level(upgrade):
        return current_user.army.upgrades.get_upgrade_level(upgrade)


class TechUpgrades:
    def __init__(self, ground_weapons: UpgradableItem, bombs: UpgradableItem, air_weapons: UpgradableItem, country: UpgradableItem):
        self.ground_weapons = ground_weapons
        self.bombs = bombs
        self.air_weapons = air_weapons
        self.country = country


TECH_UPGRADES = TechUpgrades(
    ground_weapons=UpgradableItem(
        level_1=UpgradePrice(200, 400, 600, "upgrade"),
        level_2=UpgradePrice(300, 700, 1000, "upgrade"),
        level_3=UpgradePrice(400, 900, 1600, "upgrade"),
        level_4=UpgradePrice(800, 2000, 2600, "upgrade"),
        level_5=UpgradePrice(2000, 4000, 5600, "upgrade")),
    bombs=UpgradableItem(
        level_1=UpgradePrice(200, 400, 600, "upgrade"),
        level_2=UpgradePrice(300, 700, 1000, "upgrade"),
        level_3=UpgradePrice(400, 900, 1600, "upgrade"),
        level_4=UpgradePrice(800, 2000, 2600, "upgrade"),
        level_5=UpgradePrice(2000, 4000, 5600, "upgrade")),
    air_weapons=UpgradableItem(
        level_1=UpgradePrice(200, 400, 600, "upgrade"),
        level_2=UpgradePrice(300, 700, 1000, "upgrade"),
        level_3=UpgradePrice(400, 900, 1600, "upgrade"),
        level_4=UpgradePrice(800, 2000, 2600, "upgrade"),
        level_5=UpgradePrice(2000, 4000, 5600, "upgrade")),
    country=UpgradableItem(
        level_1=UpgradePrice(200, 400, 600, "upgrade"),
        level_2=UpgradePrice(300, 700, 1000, "upgrade"),
        level_3=UpgradePrice(400, 900, 1600, "upgrade"),
        level_4=UpgradePrice(800, 2000, 2600, "upgrade"),
        level_5=UpgradePrice(2000, 4000, 5600, "upgrade")))
