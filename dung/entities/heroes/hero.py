from abc import abstractmethod
import re

import pygame
from dung.entities.entity import SPECIAL_ATTRIBUTES, Entity
from dung.monster_settings import HEROES_SETTINGS, LEVELS_SETTINGS


class Hero(Entity):
    def __init__(self, name):
        hero_settings = HEROES_SETTINGS[name.lower()]
        super().__init__(
            name.capitalize(),
            hero_settings["start-health"],
            hero_settings["start-strength"],
            hero_settings["speed"],
            weapon=hero_settings.get("start-weapon", "unarmed"),
            attacks=hero_settings.get("attacks", 1),
            shield=hero_settings.get("shield", 0),
            block=hero_settings.get("start-block-chance", 0),
            critical_hit=hero_settings.get("start-critical-hit-chance", 1)
        )
        self.skills = hero_settings["skills"]
        self.cooldowns = {}

    def _get_base_stat(self, key):
        return getattr(self, key, None) 

    def _fill_details(self, skill_index: int):
        details = self.skills[skill_index]["details"]
        data = self.skills[skill_index]["data"]

        modified_data = dict(data)
        for special_attribute in SPECIAL_ATTRIBUTES:
            if data.get(special_attribute, None) is not None:
               modified_value = self.get_modified_stat(special_attribute)
               modified_data[special_attribute] = modified_value
        def replacer(match):
            key = match.group(1)
            return str(modified_data.get(key, f"{{{{{key}}}}}"))  # keep placeholder if key not found

        return re.sub(r"\{\{(\w+)\}\}", replacer, details)

    def get_hero_skills_item(self, key: int):
        skill_index = 0
        if key == pygame.K_SPACE:
            details = self.skills[0]["details"]
            skill_index = 0
        elif key == pygame.K_q:
            # details = self.ability_item_q(self.skills[1])
            skill_index = 1
        elif key == pygame.K_w:
            # details = self.ability_item_w(self.skills[2])
            skill_index = 2
        elif key == pygame.K_e:
            # details = self.ability_item_e(self.skills[3])
            skill_index = 3
        elif key == pygame.K_r:
            # details = self.ability_item_r(self.skills[4])
            skill_index = 4
        else:
            return self.skills[0] # error?
        
        details = self._fill_details(skill_index)
        return {
            "key": self.skills[skill_index]["key"],
            "name": self.skills[skill_index]["name"], 
            "details": details,
            "data": self.skills[skill_index]["data"]
        }

    def perform_hero_action(self, enemy: Entity, key: int):
        if key == pygame.K_SPACE:
            return super().perform_basic_attack(enemy)
        elif key == pygame.K_q:
            return self.use_ability_q(self.skills[1], enemy)
        elif key == pygame.K_w:
            return self.use_ability_w(self.skills[2], enemy)
        elif key == pygame.K_e:
            return self.use_ability_e(self.skills[3], enemy)
        elif key == pygame.K_r:
            return self.use_ability_r(self.skills[4], enemy)
        else:
            return [f"{self.name} skipped his tur"] # error?

    @abstractmethod
    def use_ability_q(self, skill_item, enemy: Entity):
        pass

    @abstractmethod
    def use_ability_w(self, skill_item, enemy: Entity):
        pass

    @abstractmethod
    def use_ability_e(self, skill_item, enemy: Entity):
        pass

    @abstractmethod
    def use_ability_r(self, skill_item, enemy: Entity):
        pass

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

    def set_cooldown(self, key: int, turns: int):
        self.cooldowns[key] = { "key": key, "total_turns": turns, "turns_left": turns }

    def remove_cooldown(self, key: int):
        self.cooldowns.pop(key, None)

    def get_cooldown(self, key: int):
        return self.cooldowns.get(key, None)

    def is_skill_active(self, key: int):
        skill = self.cooldowns.get(key, None)
        return skill is None

    def clear_battle_modifiers(self):
        super().clear_battle_modifiers()
        # self.cooldowns = {} # nof deleted after fight ATM

    def tick(self):
        super().tick()
        for cooldown_key in list(self.cooldowns.keys()):
            if self.cooldowns[cooldown_key]['turns_left'] <= 1:
                self.remove_cooldown(cooldown_key)

        for cooldown in self.cooldowns.values():
            cooldown['turns_left'] -= 1