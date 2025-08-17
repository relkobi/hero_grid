from dung.entities.entity import Entity
from dung.monster_settings import MONSTERS_SETTINGS


class Monster(Entity):
    def __init__(self, monster_type: str):
        monster_settings = MONSTERS_SETTINGS[monster_type.lower()]
        super().__init__(
            name=monster_type.capitalize(),
            health=monster_settings["health"],
            strength=monster_settings["strength"],
            speed=monster_settings["speed"],
            weapon=monster_settings.get("weapon", "unarmed"),
            attacks=monster_settings.get("attacks", 1),
            shield=monster_settings.get("shield", 0),
            block=monster_settings.get("block", 0),
            critical_hit=monster_settings.get("critical_hit", 0)
        )

    def perform_monster_action(self, hero):
        return super().perform_basic_attack(hero)
