import random

import pygame
from dung.entities.entity import Entity
from dung.entities.heroes.hero import Hero
from dung.monster_settings import WEAPON_SETTINGS


class Mage(Hero):
    def __init__(self):
        super().__init__("mage")

    def use_ability_q(self, skill_item, enemy: Entity, ):
        skill_data = skill_item["data"]
        shield_bonus = skill_data["shield_bonus"]
        duration = skill_data["duration"]
        cooldown = skill_data["cooldown"]

        self.set_buff("shield", shield_bonus, duration)
        self.set_cooldown(pygame.K_q, cooldown)

        return [f"{self.name} increases their shield by {shield_bonus} for {duration} turns."]

    def use_ability_w(self, skill_item, enemy: Entity):
        skill_data = skill_item["data"]
        damage_increment = skill_data["damage_increment"]
        critical_hit_bonus = skill_data["critical_hit_bonus"]
        drawback_chance = skill_data["drawback_chance"]
        cooldown = skill_data["cooldown"]

        action_logs = self.perform_basic_attack(enemy, {"damage_increment": damage_increment, "critical_hit": critical_hit_bonus})

        if random.randint(1, 100) <= drawback_chance:
            weapon_damage = WEAPON_SETTINGS[enemy.weapon]["damage"]
            enemy_chance_attack_weapon_damage = random.randint(weapon_damage[0], weapon_damage[1])
            self.lose_health(enemy_chance_attack_weapon_damage)
            action_logs.append(f"{self.name} was harmed by {enemy.name}'s weapon for {enemy_chance_attack_weapon_damage} damage during the attack")

        self.set_cooldown(pygame.K_w, cooldown)

        return action_logs

    def use_ability_e(self, skill_item, enemy: Entity):
        skill_data = skill_item["data"]
        stun_duration = skill_data["stun_duration"]
        cooldown = skill_data["cooldown"]

        bash_damage = self.strength + self.get_buff_value("strength", 0) + self.get_debuff_value("strength", 0)
        enemy.lose_health(bash_damage)

        enemy.set_debuff("stun", 1, stun_duration)

        self.set_cooldown(pygame.K_e, cooldown)

        return [f"Knight bashed the Goblin with their shield for {bash_damage} damage and stunned it for {stun_duration} turn"]

    def use_ability_r(self, skill_item, enemy: Entity):
        skill_data = skill_item["data"]
        strength_shield_bonus = skill_data["strength_shield_bonus"]
        block_bonus = skill_data["block_bonus"]
        duration = skill_data["duration"]
        cooldown = skill_data["cooldown"]

        self.set_buff("shield", strength_shield_bonus, duration)
        self.set_buff("strength", strength_shield_bonus, duration)
        self.set_buff("block", block_bonus, duration)

        self.set_cooldown(pygame.K_r, cooldown)


        return [f"{self.name} increases their strength and defense by {strength_shield_bonus} and clock chance by {block_bonus}% for {duration} turns."]
