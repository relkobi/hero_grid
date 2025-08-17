# entity.py

import random

from dung.monster_settings import HEROES_SETTINGS, LEVELS_SETTINGS, WEAPON_SETTINGS

class Entity:
    def __init__(self, name, health, strength, speed, weapon="unarmed", attacks=1, shield=0, block=0, critical_hit=1):
        self.name = name
        self.level = 1
        self.xp = 0
        self.max_health = health
        self.health = health
        self.strength = strength
        self.speed= speed
        self.weapon = weapon
        self.attacks = attacks
        self.shield = shield
        self.block = block
        self.critical_hit = critical_hit

    def perform_basic_attack(self, other, hero_modifiers={}, enemy_modifier={}):
        weapon_damage = WEAPON_SETTINGS[self.weapon]["damage"]
        damage = 0
        attack_logs = []

        attacks_left = 1
        while attacks_left <= self.attacks:
            rnd = random.randint(weapon_damage[0], weapon_damage[1])
            attack_damage = self.strength + hero_modifiers.get("strength", 0) + rnd
            attack_damage = attack_damage * ((100 + hero_modifiers.get("damage_increment", 0)) // 100)                

            critical_hit = False
            if random.randint(1, 100) <= (self.critical_hit + hero_modifiers.get("critical_hit", 0)):
                attack_damage = attack_damage * 2
                critical_hit = True

            critical_text = "critical " if critical_hit is True else ""
            multiple_attack_text = f" (Attack {attacks_left}/{self.attacks})" if self.attacks > 1 else ""
            attack_logs.append(f"{self.name} {critical_text}hit {other.name} for {attack_damage} damage{multiple_attack_text}")
            attacks_left += 1

            blocked = False
            modified_block = other.block + enemy_modifier.get("block", 0)
            if modified_block > 0:
                if random.randint(1, 100) <= modified_block:
                    attack_damage = 0
                    blocked = True
                    attack_logs.append(f"{self.name} attack was blocked by {other.name}")
            
            if not blocked:
                modified_shield = other.shield + enemy_modifier.get("shield", 0)
                attack_damage = max(attack_damage - modified_shield, 0)
                if modified_shield > 0:
                    attack_logs.append(f"{other.name} shielded {other.shield} damage from {self.name} attack")

            damage += attack_damage

        other.lose_health(damage)
        
        # return f"{self.name} hit {self.attacks} times for total {damage} damage"
        return attack_logs

    def gain_xp(self, xp):
        self.xp += xp

        next_level_xp = LEVELS_SETTINGS[self.level]
        while self.xp >= next_level_xp:
            self.xp -= next_level_xp
            self.gain_level()
            next_level_xp = LEVELS_SETTINGS[self.level]

    def gain_level(self):
        hero_settings = HEROES_SETTINGS[self.name.lower()]
        
        self.level += 1
        self.max_health += hero_settings["level-health"]
        self.health += hero_settings["level-health"]
        self.strength += hero_settings["level-strength"]
        self.block += hero_settings["level-block-chance"]

    def get_damage_string(self):
        weapon_damage = WEAPON_SETTINGS[self.weapon]["damage"]
        min_damage = (self.strength + weapon_damage[0]) * self.attacks
        max_damage = (self.strength + weapon_damage[1]) * self.attacks

        return f"{min_damage}-{max_damage}"

    def gain_health(self, health):
        self.health = min(self.max_health, self.health + health)

    def lose_health(self, health):
        self.health = max(0, self.health - health)