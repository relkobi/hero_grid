import random

import pygame
from dung.battle_exceptions.hero_evaded_battle_exception import HeroEvadedBattleException
from dung.entities.entity import Entity
from dung.entities.heroes.hero import Hero
from dung.monster_settings import WEAPON_SETTINGS


class Rogue(Hero):
    def __init__(self):
        super().__init__("rogue")

    def use_ability_q(self, skill_item, enemy: Entity, ):
        skill_data = skill_item["data"]
        cooldown = skill_data["cooldown"]

        self.set_cooldown(pygame.K_q, cooldown)

        modifiers={"attack_base_damage": self.speed + self.get_buff_combine_value("speed", 0)}
        return self.perform_basic_attack(enemy, modifiers)

    def use_ability_w(self, skill_item, enemy: Entity):
        skill_data = skill_item["data"]
        evade_duration = skill_data["evade_duration"]
        cooldown = skill_data["cooldown"]

        self.set_buff("evade", 1, evade_duration)
        self.set_cooldown(pygame.K_w, cooldown)

        return [f"Rouge will evade all the atacks until his next turn"]

    def use_ability_e(self, skill_item, enemy: Entity):
        skill_data = skill_item["data"]
        poison_stacks = skill_data["poison_stacks"]
        poison_duration = skill_data["poison_duration"]
        cooldown = skill_data["cooldown"]

        self.set_buff("poison", poison_stacks, poison_duration)
        self.set_cooldown(pygame.K_e, cooldown)

        return [f"Rouge poisened his weapons to add {poison_stacks} for the next {poison_duration} turns"]

    def use_ability_r(self, skill_item, enemy: Entity):
        skill_data = skill_item["data"]
        cooldown = skill_data["cooldown"]

        super().set_cooldown(pygame.K_r, cooldown)
        raise HeroEvadedBattleException([f"{self.name} fleed from the battle."])
