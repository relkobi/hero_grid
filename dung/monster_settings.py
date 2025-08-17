MONSTERS_SETTINGS = {
    "goblin": {
        "level": 1,
        "health": 15,
        "strength": 2,
        "weapon": "dagger",
        "xp": 4,
        "speed": 3,
        "attacks": 1,
        "shield": 0,
        "critical-hit": 0,
        "block": 0,
    },
    "skeleton": {
        "level": 1,
        "health": 18,
        "strength": 2,
        "weapon": "short-sword",
        "xp": 6,
        "speed": 2,
        "attacks": 1,
        "shield": 0,
        "critical-hit": 0,
        "block": 0,
    }
}

WEAPON_SETTINGS = {
    "unarmed": {
        "damage": [1,1]
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
        "start-strength": 5,
        "start-weapon": "long-sword",
        "start-block-chance": 7,
        "start-critical-hit-chance": 1,
        "attacks": 1,
        "shield": 1,
        "speed": 3,
        "level-health": 10,
        "level-strength": 3,
        "level-block-chance": 1,
        "level-critical-hit-chance": 1,
        "info": "Knight uses his shield to mitigate incoming damage with a chance to completely block it"
    },
    "rogue": {
        "is-active": True,
        "start-health": 12,
        "start-strength": 3,
        "start-weapon": "dagger",
        "start-block-chance": 0,
        "start-critical-hit-chance": 10,
        "attacks": 2,
        "shield": 0,
        "speed": 5,
        "level-health": 6,
        "level-strength": 2,
        "level-block-chance": 0,
        "level-critical-hit-chance": 1,
        "info": "Rogue uses his speed and skill to hit more than once on each attack and have increased chances to double the attack damage"
    },
    "mage": {
        "is-active": False,
        "start-health": 10,
        "start-strength": 2,
        "start-weapon": "staff",
        "start-block-chance": 0,
        "start-critical-hit-chance": 2,
        "attacks": 1,
        "shield": 0,
        "speed": 3,
        "level-health": 5,
        "level-strength": 1,
        "level-block-chance": 0,
        "level-critical-hit-chance": 0,
        "info": "Mage currently have no special skills"
    }
}

LEVELS_SETTINGS = [0, 10, 15, 20, 30, 50, 80, 120, 200, 300]
