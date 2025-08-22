import pygame
from dung.monster_settings import *
from dung.size_settings import SIZES
from dung.utils import resource_path
from dung.game_settings import game_settings

IMAGES_BASE_PATH = "dung/assets/images"
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
            hero_img = pygame.image.load(resource_path(f"{IMAGES_BASE_PATH}/{hero}.png")).convert_alpha()
            hero_img = pygame.transform.scale(hero_img, (SIZES.TILE_SIZE, SIZES.TILE_SIZE))
            self.heroes[hero] = hero_img

        self.monsters = {}
        for monster in MONSTERS_SETTINGS.keys():
            monster_image = pygame.image.load(resource_path(f"{IMAGES_BASE_PATH}/{monster}.png")).convert_alpha()
            monster_image = pygame.transform.scale(monster_image, (SIZES.TILE_SIZE, SIZES.TILE_SIZE))
            self.monsters[monster] = monster_image

        misc_items = ["health_potion", "campfire", "chest"]
        self.misc = {}
        for item in misc_items:
            item_image = pygame.image.load(resource_path(f"{IMAGES_BASE_PATH}/{item}.png")).convert_alpha()
            item_image = pygame.transform.scale(item_image, (SIZES.TILE_SIZE, SIZES.TILE_SIZE))
            self.misc[item] = item_image

        tiles_types = ["grass_tile"]
        self.tiles = {}
        for tile in tiles_types:
            tile_image = pygame.image.load(resource_path(f"{IMAGES_BASE_PATH}/{tile}.png")).convert()
            tile_image = pygame.transform.scale(tile_image, (SIZES.TILE_SIZE, SIZES.TILE_SIZE))
            self.tiles[tile] = tile_image

        skills_names = ["attack", "defend"]
        self.skills = {}
        for skill_name in skills_names:
            skill_image = pygame.image.load(resource_path(f"{IMAGES_BASE_PATH}/skills/{skill_name}.png")).convert_alpha()
            skill_image = pygame.transform.scale(skill_image, (SIZES.TILE_SIZE, SIZES.TILE_SIZE))
            self.skills[skill_name] = skill_image


    def update_by_resolution(self):
        self._reload_images()

IMAGES = ImagesSettings(game_settings.resolution[0], game_settings.resolution[1])
