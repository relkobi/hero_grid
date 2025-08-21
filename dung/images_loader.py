import pygame
from dung.monster_settings import HEROES_SETTINGS
from dung.size_settings import SIZES
from dung.utils import resource_path
from dung.game_settings import game_settings

HEADER_SECTION_RATIO = 0.15
SIDEBAR_SECTION_RATIO = 0.3

class ImagesSettings:
    _instance = None

    def __new__(cls, screen_width=None, screen_height=None):
        if cls._instance is None:
            if screen_width is None or screen_height is None:
                raise ValueError("screen_width and screen_height must be provided on first creation")
            cls._instance = super(ImagesSettings, cls).__new__(cls)
            cls._instance._reload_images()
        return cls._instance

    def _reload_images(self):
        self.heroes = {}
        for hero in HEROES_SETTINGS.keys():
            hero_img = pygame.image.load(resource_path(f"dung/assets/{hero}.png"))
            hero_img = pygame.transform.scale(hero_img, (SIZES.TILE_SIZE, SIZES.TILE_SIZE))
            self.heroes[hero] = hero_img

        goblin_img = pygame.image.load(resource_path("dung/assets/goblin.png"))
        goblin_img = pygame.transform.scale(goblin_img, (SIZES.TILE_SIZE, SIZES.TILE_SIZE))
        skeleton_img = pygame.image.load(resource_path("dung/assets/skeleton.png"))
        skeleton_img = pygame.transform.scale(skeleton_img, (SIZES.TILE_SIZE, SIZES.TILE_SIZE))
        self.monsters = {
            "goblin":goblin_img,
            "skeleton": skeleton_img
        }
        
        health_potion_img = pygame.image.load(resource_path("dung/assets/health_potion.png"))
        health_potion_img = pygame.transform.scale(health_potion_img, (SIZES.TILE_SIZE, SIZES.TILE_SIZE))
        campfire_img = pygame.image.load(resource_path("dung/assets/campfire.png"))
        campfire_img = pygame.transform.scale(campfire_img, (SIZES.TILE_SIZE, SIZES.TILE_SIZE))
        self.misc = {
            "health_potion": health_potion_img,
            "campfire": campfire_img
        }

    def update_by_resolution(self):
        self._reload_images()

IMAGES = ImagesSettings(game_settings.resolution[0], game_settings.resolution[1])
