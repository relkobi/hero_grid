# entity.py

import random

from dung.monster_settings import HEROES_SETTINGS, LEVELS_SETTINGS, WEAPON_SETTINGS

SPECIAL_ATTRIBUTES = ["strength", "speed", "shield", "block", "critical-hit"]
DOT_DEBUFFS = ["poison"]
MERGED_BUFFS = ["stun"]
STACKED_BUFFS = []

class Entity:
    def __init__(self, name, health, strength, speed, magic, weapon="unarmed", attacks=1, shield=0, block=0, critical_hit=1):
        self.name = name
        self.level = 1
        self.xp = 0
        self.max_health = health
        self.health = health
        self.strength = strength
        self.speed = speed
        self.magic = magic
        self.weapon = weapon
        self.attacks = attacks
        self.shield = shield
        self.block = block
        self.critical_hit = critical_hit
        self.buffs = []
        self.debuffs = []

    def _get_base_stat(self, key):
        return getattr(self, key, None) 

    def get_modified_stat(self, key):
        base_value = self._get_base_stat(key)
        value_modifier = 0
        if key in SPECIAL_ATTRIBUTES:
            value_modifier = self.get_buff_combine_value(key, value_modifier)

        return base_value + value_modifier

    def pre_turn_check(self):
        is_stunned = self.get_debuff_value("stun", 0) > 0
        battle_logs = []
        turn_ended = False
        if is_stunned:
            battle_logs.append(f"{self.name} is stunned and skips their turn.")
            turn_ended = True

        return turn_ended, battle_logs

    def perform_basic_attack(self, other, hero_modifiers={}, enemy_modifier={}):
        weapon_damage = WEAPON_SETTINGS[self.weapon]["damage"]
        damage = 0
        attack_logs = []

        attacks_left = 1
        current_strength = self.strength + self.get_buff_combine_value("strength", 0) + hero_modifiers.get("strength", 0)
        attack_base_damage = current_strength if hero_modifiers.get("attack_base_damage", None) is None else hero_modifiers["attack_base_damage"]
        while attacks_left <= self.attacks:
            rnd = random.randint(weapon_damage[0], weapon_damage[1])
            attack_damage = attack_base_damage + rnd
            attack_damage = attack_damage * ((100 + hero_modifiers.get("damage_increment", 0)) // 100)                

            critical_hit = False
            if random.randint(1, 100) <= (self.critical_hit + self.get_buff_combine_value("critical_hit", 0) + hero_modifiers.get("critical_hit", 0)):
                attack_damage = attack_damage * 2
                critical_hit = True

            critical_text = "critical " if critical_hit is True else ""
            multiple_attack_text = f" (Attack {attacks_left}/{self.attacks})" if self.attacks > 1 else ""
            attack_logs.append(f"{self.name} {critical_text}hit {other.name} for {attack_damage} damage{multiple_attack_text}")
            attacks_left += 1

            attack_failed = False
            if other.get_buff_value("evade", 0) > 0:
                attack_failed =  True
                attack_logs.append(f"{self.name}'s attack was evaded by {other.name}")

            modified_block = other.block + other.get_buff_combine_value("block", 0) + enemy_modifier.get("block", 0)
            if not attack_failed and modified_block > 0:
                if random.randint(1, 100) <= modified_block:
                    attack_failed = True
                    attack_logs.append(f"{self.name} attack was blocked by {other.name}")
     
            elif not attack_failed:
                modified_shield = max(0, other.shield + other.get_buff_combine_value("shield", 0), enemy_modifier.get("shield", 0))
                attack_damage = max(attack_damage - modified_shield, 0)
                if modified_shield > 0:
                    attack_logs.append(f"{other.name} shielded {modified_shield} damage from {self.name} attack")

            if attack_failed:
                attack_damage = 0
            else:
                for dot_name in DOT_DEBUFFS:
                    dot_value = self.get_buff_value(dot_name, 0)
                    if dot_value > 0:
                        other.set_debuff(dot_name, dot_value, dot_value)

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
        tick_messages = []
        dots = {}
        for debuff in self.debuffs:
            if debuff["name"] in DOT_DEBUFFS:
                debuff_name = debuff["name"]
                debuff_value = debuff["value"]
                debuff["value"] -= 1

                if dots.get(debuff_name, None) is None:
                    dots[debuff_name] = debuff_value
                else:
                    dots[debuff_name] += debuff_value

        for dot_name, dot_value in dots.items():
            self.lose_health(dot_value)
            tick_messages.append(f"{self.name} gain {dot_value} damage from {dot_name}")

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

        return tick_messages