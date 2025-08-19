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
        self.buffs = []
        self.debuffs = []

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
            if random.randint(1, 100) <= (self.critical_hit + self.get_buff_combine_value("critical_hit", 0) + hero_modifiers.get("critical_hit", 0)):
                attack_damage = attack_damage * 2
                critical_hit = True

            critical_text = "critical " if critical_hit is True else ""
            multiple_attack_text = f" (Attack {attacks_left}/{self.attacks})" if self.attacks > 1 else ""
            attack_logs.append(f"{self.name} {critical_text}hit {other.name} for {attack_damage} damage{multiple_attack_text}")
            attacks_left += 1

            blocked = False
            modified_block = other.block + other.get_buff_combine_value("block", 0) + enemy_modifier.get("block", 0)
            if modified_block > 0:
                if random.randint(1, 100) <= modified_block:
                    attack_damage = 0
                    blocked = True
                    attack_logs.append(f"{self.name} attack was blocked by {other.name}")
            
            if not blocked:
                modified_shield = max(0, other.shield + other.get_buff_combine_value("shield", 0), enemy_modifier.get("shield", 0))
                attack_damage = max(attack_damage - modified_shield, 0)
                if modified_shield > 0:
                    attack_logs.append(f"{other.name} shielded {modified_shield} damage from {self.name} attack")

            damage += attack_damage

        other.lose_health(damage)
        
        # return f"{self.name} hit {self.attacks} times for total {damage} damage"
        return attack_logs

    def get_damage_string(self):
        weapon_damage = WEAPON_SETTINGS[self.weapon]["damage"]
        modified_strenght = self.strength + self.get_buff_combine_value("strength", 0)
        min_damage = (modified_strenght + weapon_damage[0]) * self.attacks
        max_damage = (modified_strenght + weapon_damage[1]) * self.attacks

        return f"{min_damage}-{max_damage}"

    def gain_health(self, health):
        self.health = min(self.max_health, self.health + health)

    def lose_health(self, health):
        self.health = max(0, self.health - health)

    def set_buff(self, name: str, value: int, turns: int):
        self.buffs.append({ "name": name, "value": value, "turns": turns })

    def get_buff_value(self, name: str, default_value: int):
        buff_value = default_value
        for buff in self.buffs:
            if buff.get("name", None) == name:
                buff_value += buff["value"]
        
        return buff_value

    def set_debuff(self, name: str, value: int, turns: int):
        self.debuffs.append({ "name": name, "value": value, "turns": turns })


    def get_debuff_value(self, name: str, default_value: int):
        debuff_value = default_value
        for debuff in self.debuffs:
            if debuff.get("name", None) == name:
                debuff_value += debuff["value"]
        
        return debuff_value

    def get_buff_combine_value(self, name: str, default_value: int):
        combined_value = default_value
        combined_value += self.get_buff_value(name, default_value)
        combined_value -= self.get_debuff_value(name, default_value)

        return combined_value

    def clear_battle_modifiers(self):
        self.buffs = []
        self.debuffs = []

    def tick(self):
        self.buffs = [
            {**buff, "turns": buff["turns"] - 1}
            for buff in self.buffs
            if buff["turns"] > 1
        ]

        self.debuffs = [
            {**debuff, "turns": debuff["turns"] - 1}
            for debuff in self.debuffs
            if debuff["turns"] > 1
        ]