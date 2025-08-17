from abc import abstractmethod

import pygame
from dung.entities.entity import Entity
from dung.monster_settings import HEROES_SETTINGS


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
    def use_ability_q(self, enemy: Entity, data={}):
        pass

    @abstractmethod
    def use_ability_w(self, enemy: Entity, data={}):
        pass

    @abstractmethod
    def use_ability_e(self, enemy: Entity, data={}):
        pass

    @abstractmethod
    def use_ability_r(self, enemy: Entity, data={}):
        pass