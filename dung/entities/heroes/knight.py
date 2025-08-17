import random
from dung.entities.entity import Entity
from dung.entities.heroes.hero import Hero
from dung.monster_settings import WEAPON_SETTINGS


class Knight(Hero):
    def __init__(self):
        super().__init__("knight")

    def use_ability_q(self, enemy: Entity, data={}):
        defense_value = 2
        buff_turns = 3
        #TODO apply the buff

        return [f"{self.name} increases their defense by {defense_value} for {buff_turns} turns."]

    def use_ability_w(self, enemy: Entity, data={}):
        #TODO handle CD on all skills
        action_logs = self.perform_basic_attack(enemy, {"damage_increment": 50, "critical_hit": 15})
        
        #enemy_chance_attack
        if random.randint(1, 100) <= 99:
            weapon_damage = WEAPON_SETTINGS[enemy.weapon]["damage"]
            enemy_chance_attack_weapon_damage = random.randint(weapon_damage[0], weapon_damage[1])
            self.lose_health(enemy_chance_attack_weapon_damage)
            action_logs.append(f"{self.name} was harmed by {enemy.name}'s weapon for {enemy_chance_attack_weapon_damage} damage during the attack")
      
        return action_logs

    def use_ability_e(self, enemy: Entity, data={}):
        bash_damage = self.strength #TODO modifiers?
        enemy.lose_health(bash_damage) # modifiers?
        #TODO apply stun on enemy
        stun_duration = 1

        return [f"Knight bashed the Goblin with their shield for {bash_damage} damage and stunned it for {stun_duration} turn"]

    def use_ability_r(self, enemy: Entity, data={}):
        defense_value = 2
        block_bonus = 10
        buff_turns = 4
        #TODO apply the buff

        return [f"{self.name} increases their strength and defense by {defense_value} and clock chance by {block_bonus}% for {buff_turns} turns."]

        #     skill_details = [
        #     "Perform a basic attack.",
        #     q "Increases defense value for the next 3 turns.",
        #     w "A swift attack that deals increased damage with a higher chance to critically hit. There is a chance you may be hit by the enemy's weapon during the attack.",
        #     e "Use your shield to strike the enemy for [str] damage and stun them for 1 turn.",
        #     r "Increase your strength and defense by 2, and your block chance by 10% for 4 turns."
        # ]
        # keys = ["SPACE", "Q", "W", "E", "R"]