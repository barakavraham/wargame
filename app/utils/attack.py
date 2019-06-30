from random import uniform
from typing import Optional
from dataclasses import dataclass
from app import db
from app.utils.shop import SHOP_ITEMS


@dataclass
class BattleResults:
    attacker_results: dict
    attacked_results: dict
    is_winner: Optional[bool]


def stronger_army_by_unit(attacker_army, attacked_army, unit_type):
    if attacker_army.get_power(unit_type) > attacked_army.get_power(unit_type):
        return attacker_army
    elif attacked_army.get_power(unit_type) > attacker_army.get_power(unit_type):
        return attacked_army
    return None


def get_weapons_in_unit(unit_type):
    return [weapon for weapon in SHOP_ITEMS if SHOP_ITEMS[weapon].weapon_type == unit_type]


def attack_weapon(attacker_army, attacker_chance, attacked_army, attacked_chance, weapon, battle_results):
    attacker_army_current_amount = attacker_army.get_item_amount(weapon)
    attacked_army_current_amount = attacked_army.get_item_amount(weapon)
    if attacker_army_current_amount < attacked_army_current_amount:
        weapon_amount = attacker_army.get_item_amount(weapon)
    else:
        weapon_amount = attacked_army.get_item_amount(weapon)
    attacker_weapon_lost = weapon_amount - round(weapon_amount * ((100 - attacked_chance) / 100))
    attacked_weapon_lost = weapon_amount - round(weapon_amount * ((100 - attacker_chance) / 100))
    setattr(attacker_army, weapon, attacker_army_current_amount - attacker_weapon_lost)
    setattr(attacked_army, weapon, attacked_army_current_amount - attacked_weapon_lost)
    battle_results.attacker_results[weapon] = attacker_weapon_lost
    battle_results.attacked_results[weapon] = attacked_weapon_lost
    db.session.commit()

    # 0 - Attacker army won
    # 1 - Attacked army won
    # 2 - Tie
    return (0 if battle_results.attacker_results[weapon] < battle_results.attacked_results[weapon]
            else 1 if battle_results.attacked_results[weapon] < battle_results.attacker_results[weapon]
            else 2)


def attack(attacker_army, attacked_army, unit_types=None):
    battle_results = BattleResults(attacker_results={}, attacked_results={}, is_winner=None)
    attacker_army_counter = 0
    attacked_army_counter = 0
    if unit_types is None:
        unit_types = set([SHOP_ITEMS[weapon].weapon_type for weapon in SHOP_ITEMS])
    for unit_type in unit_types:
        stronger_army = stronger_army_by_unit(attacker_army, attacked_army, unit_type)
        for weapon in get_weapons_in_unit(unit_type):
            if stronger_army and stronger_army == attacker_army:
                attacker_chance = uniform(2.0, 3.0)
                attacked_chance = uniform(1.0, 2.0)
            elif stronger_army:
                attacker_chance = uniform(1.0, 2.0)
                attacked_chance = uniform(2.0, 3.0)
            else:
                attacker_chance = uniform(1.5, 2.5)
                attacked_chance = uniform(1.5, 2.5)
            result = attack_weapon(attacker_army=attacker_army,
                                   attacker_chance=attacker_chance,
                                   attacked_army=attacked_army,
                                   attacked_chance=attacked_chance,
                                   weapon=weapon,
                                   battle_results=battle_results)
            if result == 0:
                attacker_army_counter += 1
            elif result == 1:
                attacked_army_counter += 1
    battle_results.is_winner = (True if attacker_army_counter > attacked_army_counter
                                else False if attacked_army_counter > attacker_army_counter else None)
    return battle_results
