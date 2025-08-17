import pygame
from dung.utils import resource_path
from dung.game_settings import game_settings


class FontSettings:
    _instance = None

    def __new__(cls, font_name=None, screen_height=None):
        if cls._instance is None:
            if font_name is None or screen_height is None:
                raise ValueError("font_name and screen_height must be provided on first creation")
            cls._instance = super(FontSettings, cls).__new__(cls)
            cls._instance._calculate_fonts_values(font_name, screen_height)
        return cls._instance

    def _calculate_fonts_values(self, font_name, screen_height: int):
        self.FONT_NAME = font_name

        font_path = resource_path(f"dung/assets/fonts/{self.FONT_NAME}")

        self.TEXT_FONT = pygame.font.Font(font_path, round(screen_height * 0.02))
        self.TITLE_FONT = pygame.font.Font(font_path, round(screen_height * 0.035))
        self.MEDUIM_FONT = pygame.font.Font(font_path, round(screen_height * 0.06))
        self.LARGE_FONT = pygame.font.Font(font_path, round(screen_height * 0.12))
        self.START_FONT = pygame.font.Font(font_path, round(screen_height * 0.20))

    def resize_fonts(self, font_name, screen_height: int):
        self._calculate_fonts_values(font_name, screen_height)

FONTS = FontSettings(game_settings.font_name, game_settings.resolution[1])
