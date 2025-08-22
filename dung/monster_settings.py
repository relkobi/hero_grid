import pygame


MONSTERS_SETTINGS = {
    "goblin": {
        "level": 1,
        "health": 15,
        "strength": 2,
        "speed": 3,
        "magic": 0,
        "weapon": "dagger",
        "xp": 4,
        "attacks": 1,
        "shield": 0,
        "critical-hit": 0,
        "block": 0,
    },
    "skeleton": {
        "level": 1,
        "health": 18,
        "strength": 2,
        "speed": 2,
        "magic": 0,
        "weapon": "short-sword",
        "xp": 6,
        "attacks": 1,
        "shield": 0,
        "critical-hit": 0,
        "block": 0,
    },
    "mimic_chest": {
        "level": 3,
        "health": 32,
        "strength": 6,
        "speed": 5,
        "magic": 0,
        "weapon": "teeth",
        "xp": 20,
        "attacks": 1,
        "shield": 1,
        "critical-hit": 10,
        "block": 0,
    }
}

WEAPON_SETTINGS = {
    "unarmed": {
        "damage": [1,1]
    },
    "teeth": {
        "damage": [4,6]
    },
    "dagger": {
        "damage": [1,4]
    },
    "staff": {
        "damage": [2, 5]
    },
    "short-sword": {
        "damage": [1,6]
    },
    "long-sword": {
        "damage": [1,8]
    }
}

HEROES_SETTINGS = {
    "knight": {
        "is-active": True,
        "start-health": 20,
        "start-strength": 4,
        "start-speed": 2,
        "start-magic": 1,        
        "start-weapon": "long-sword",
        "start-block-chance": 7,
        "start-critical-hit-chance": 1,
        "attacks": 1,
        "shield": 1,
        "level-health": 10,
        "level-strength": 2,
        "level-speed": 1,
        "level-magic": 0,
        "level-block-chance": 1,
        "level-critical-hit-chance": 1,
        "info": "Knight uses his shield to mitigate incoming damage with a chance to completely block it",
        "skills": [
            {
                "key": pygame.K_SPACE,
                "name": "Attack", 
                "details": "Perform a basic attack",
                "data": {
                    "cooldown": -1
                }
            },
            {
                "key": pygame.K_q,
                "name": "Defense",
                "details": "Increases shield by {{shield_bonus}} for the next {{duration}} turns.",
                "data": {
                    "shield_bonus": 1,
                    "duration": 4,
                    "cooldown": 4
                }
            },
            {
                "key": pygame.K_w,
                "name": "Reckless Attack",
                "details": "A swift attack that deals increased damage by {{damage_increment}}% with a critically hit bonus of {{critical_hit_bonus}}. There is a {{drawback_chance}}% you may be hit by the enemy's weapon during the attack.",
                "data": {
                    "damage_increment": 50,
                    "critical_hit_bonus": 15,
                    "drawback_chance": 50,
                    "cooldown": 4
                }
            },
            {
                "key": pygame.K_e,
                "name": "Bash", 
                "details": "Use your shield to strike the enemy for {{strength}} damage and stun them for {{stun_duration}} turn.",
                "data": {
                    "strength": 0,
                    "stun_duration": 1,
                    "cooldown": 4
                }
            },
            {
                "key": pygame.K_r,
                "name": "Concentrate", 
                "details": "Increase your strength and defense by {{strength_shield_bonus}}, and your block chance by {{block_bonus}}% for {{duration}} turns.",
                "data": {
                    "strength_shield_bonus": 2,
                    "block_bonus": 10,
                    "duration": 4,
                    "cooldown": 4
                }
            }
        ]
    },
    "rogue": {
        "is-active": True,
        "start-health": 12,
        "start-strength": 2,
        "start-speed": 4,
        "start-magic": 1,   
        "start-weapon": "dagger",
        "start-block-chance": 0,
        "start-critical-hit-chance": 10,
        "attacks": 2,
        "shield": 0,
        "level-health": 6,
        "level-strength": 1,
        "level-speed": 2,
        "level-magic": 0,
        "level-block-chance": 0,
        "level-critical-hit-chance": 1,
        "info": "Rogue uses his speed and skill to hit more than once on each attack and have increased chances to double the attack damage",
        "skills": [
            {
                "key": pygame.K_SPACE,
                "name": "Attack", 
                "details": "Perform a basic attack using both of your weapons.",
                "data": {
                    "cooldown": -1
                }
            },
            {
                "key": pygame.K_q,
                "name": "Swift Attack",
                "details": "Quickly hit your enemy using your {{speed}} as the baseline for this attack.",
                "data": {
                    "speed": 0,
                    "cooldown": 4
                }
            },
            {
                "key": pygame.K_w,
                "name": "Evade",
                "details": "Enter a heightened state of agility, evading all attacks until your next turn.",
                "data": {
                    "evade_duration": 1,
                    "cooldown": 4
                }
            },
            {
                "key": pygame.K_e,
                "name": "Poisoned Weapon", 
                "details": "Poison your weapons, adding {{poison_stacks}} poison damage to each attack for the next {{poison_duration}} turns.",
                "data": {
                    "poison_stacks": 2,
                    "poison_duration": 2,
                    "cooldown": 5
                }
            },
            {
                "key": pygame.K_r,
                "name": "Smoking Mask",
                "details": "Throw a smoke bomb to instantly flee from the fight, ending combat immediately.",
                "data": {
                    "cooldown": 20
                }
            }
        ]
    },
    "mage": {
        "is-active": False,
        "start-health": 10,
        "start-strength": 1,
        "start-speed": 2,
        "start-magic": 4,  
        "start-weapon": "staff",
        "start-block-chance": 0,
        "start-critical-hit-chance": 2,
        "attacks": 1,
        "shield": 0,
        "level-health": 5,
        "level-strength": 0,
        "level-speed": 1,
        "level-magic": 2,
        "level-block-chance": 0,
        "level-critical-hit-chance": 0,
        "info": "Mage currently have no special skills",
                "skills": [
            {
                "key": pygame.K_SPACE,
                "name": "Attack", 
                "details": "Perform a basic attack",
                "data": {}
            },
            {
                "key": pygame.K_q,
                "name": "Defense",
                "details": "Increases shield by {{shield_bonus}} for the next {{duration}} turns.",
                "data": {
                    "shield_bonus": 1,
                    "duration": 4,
                    "cooldown": 4
                }
            },
            {
                "key": pygame.K_w,
                "name": "Reckless Attack",
                "details": "A swift attack that deals increased damage by {{damage_increment}}% with a critically hit bonus of {{critical_hit_bonus}}. There is a {{drawback_chance}}% you may be hit by the enemy's weapon during the attack.",
                "data": {
                    "damage_increment": 50,
                    "critical_hit_bonus": 15,
                    "drawback_chance": 50,
                    "cooldown": 4
                }
            },
            {
                "key": pygame.K_e,
                "name": "Bash", 
                "details": "Use your shield to strike the enemy for {{strength}} damage and stun them for {{stun_duration}} turn.",
                "data": {
                    "strength": 0,
                    "stun_duration": 1,
                    "cooldown": 4
                }
            },
            {
                "key": pygame.K_r,
                "name": "Concentrate", 
                "details": "Increase your strength and defense by {{strength_shield_bonus}}, and your block chance by {{block_bonus}}% for {{duration}} turns.",
                "data": {
                    "strength_shield_bonus": 2,
                    "block_bonus": 10,
                    "duration": 4,
                    "cooldown": 4
                }
            }
        ]
    }
}

LEVELS_SETTINGS = [0, 10, 15, 20, 30, 50, 80, 120, 200, 300]
