from abc import abstractmethod

import pygame
from dung.entities.entity import Entity
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
        self.cooldowns = {}

    def perform_hero_action(self, enemy: Entity, key: None):
        if key == pygame.K_SPACE:
            return super().perform_basic_attack(enemy)
        elif key == pygame.K_q:
            return self.use_ability_q(enemy)
        elif key == pygame.K_w:
            return self.use_ability_w(enemy)
        elif key == pygame.K_e:
            return self.use_ability_e(enemy)
        elif key == pygame.K_r:
            return self.use_ability_r(enemy)
        else:
            return [f"{self.name} skipped his tur"] # error?

    @abstractmethod
    def use_ability_q(self, enemy: Entity):
        pass

    @abstractmethod
    def use_ability_w(self, enemy: Entity):
        pass

    @abstractmethod
    def use_ability_e(self, enemy: Entity):
        pass

    @abstractmethod
    def use_ability_r(self, enemy: Entity):
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