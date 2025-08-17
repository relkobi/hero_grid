import pygame

from dung.font_settings import FONTS
from dung.ui.components.settings_items import draw_settings_items
from dung.settings import *
from dung.size_settings import SIZES


def draw_settings_menu(screen, event_list):
    # Overlay
    overlay = pygame.Surface((SIZES.WIDTH + SIZES.SIDEBAR_SECTION_SIZE, SIZES.HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))  # RGBA: 150 is opacity (0 = transparent, 255 = opaque)
    screen.blit(overlay, (0, SIZES.HEADER_SECTION_SIZE))

    # Popup Frame
    x_center = int(screen.get_width() // 2)
    options_rect = pygame.Rect(0, 0, max(int(screen.get_width() * 0.7), 800), min(SIZES.SCREEN_HEIGHT - SIZES.HEADER_SECTION_SIZE * 2, max(screen.get_height() * 0.8, 600)))
    options_rect.center = (x_center, (screen.get_height() - SIZES.HEADER_SECTION_SIZE) // 2 + SIZES.HEADER_SECTION_SIZE)

    pygame.draw.rect(screen, WHITE, options_rect, border_radius=10)
    pygame.draw.rect(screen, BLACK, options_rect, border_radius=10, width=5)

    y_offset = options_rect.y + FONTS.LARGE_FONT.get_height() // 2 + 10

    draw_settings_items(screen, event_list, x_center, y_offset)