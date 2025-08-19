import random

import pygame
from dung.entities.entity import Entity
from dung.entities.heroes.hero import Hero
from dung.monster_settings import WEAPON_SETTINGS


class Knight(Hero):
    def __init__(self):
        super().__init__("knight")

    def use_ability_q(self, enemy: Entity):
        shield_value = 2
        buff_turns = 3

        super().set_buff("shield", shield_value, buff_turns)
        super().set_cooldown(pygame.K_q, buff_turns)

        return [f"{self.name} increases their defense by {shield_value} for {buff_turns} turns."]

    def use_ability_w(self, enemy: Entity):
        #TODO handle CD on all skills
        action_logs = self.perform_basic_attack(enemy, {"damage_increment": 50, "critical_hit": 15})
        
        #enemy_chance_attack
        if random.randint(1, 100) <= 99:
            weapon_damage = WEAPON_SETTINGS[enemy.weapon]["damage"]
            enemy_chance_attack_weapon_damage = random.randint(weapon_damage[0], weapon_damage[1])
            self.lose_health(enemy_chance_attack_weapon_damage)
            action_logs.append(f"{self.name} was harmed by {enemy.name}'s weapon for {enemy_chance_attack_weapon_damage} damage during the attack")

        super().set_cooldown(pygame.K_w, 2)

        return action_logs

    def use_ability_e(self, enemy: Entity):
        bash_damage = self.strength + self.get_buff_value("strength", 0) + self.get_debuff_value("strength", 0)
        enemy.lose_health(bash_damage)

        stun_duration = 1
        enemy.set_debuff("stun", 1, stun_duration)

        super().set_cooldown(pygame.K_e, 3)

        return [f"Knight bashed the Goblin with their shield for {bash_damage} damage and stunned it for {stun_duration} turn"]

    def use_ability_r(self, enemy: Entity):
        strength_shield_value = 2
        block_bonus = 10
        buff_turns = 4

        self.set_buff("shield", strength_shield_value, buff_turns)
        self.set_buff("strength", strength_shield_value, buff_turns)
        self.set_buff("block", block_bonus, buff_turns)

        super().set_cooldown(pygame.K_r, buff_turns)


        return [f"{self.name} increases their strength and defense by {strength_shield_value} and clock chance by {block_bonus}% for {buff_turns} turns."]
