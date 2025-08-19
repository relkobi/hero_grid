# credits.py

import pygame
from dung.font_settings import FONTS
from dung.settings import BLACK, WHITE
from dung.size_settings import SIZES

credits_lines = [
    "Thank you for playing Hero Grid!",
    "",
    "Game Design", "Ran", "",
    "Programming", "Ran", "",
    "Art", "Ran", "",
    "Music", "Random", "",
    "Special Thanks", "Tuti", "Ofear", "",
    "The End",
    "", "", "", ""
]

class CreditsScreen:
    def __init__(self):
        self.width, self.height = SIZES.SCREEN_WIDTH, SIZES.SCREEN_HEIGHT
        self.font = FONTS.MEDUIM_FONT
        self.scroll_speed = 2

        self.surface, self.total_height = self._create_surface()
        self.scroll_y = self.height  # Start from bottom

    def _create_surface(self):
        line_height = self.font.get_linesize()
        surface_height = line_height * len(credits_lines)
        surface = pygame.Surface((self.width, surface_height), pygame.SRCALPHA)
        x_center = SIZES.SCREEN_WIDTH // 2

        for i, line in enumerate(credits_lines):
            rendered = self.font.render(line, True, WHITE)
            rect = rendered.get_rect()
            rect.centerx = x_center
            rect.top = i * line_height
            surface.blit(rendered, rect)

        return surface, surface_height

    def reset(self):
        self.scroll_y = self.height

    def update_and_draw(self, screen):
        screen.fill(BLACK)
        screen.blit(self.surface, (0, self.scroll_y))
        self.scroll_y -= self.scroll_speed

    def is_finished(self):
        return self.scroll_y < -self.total_height
