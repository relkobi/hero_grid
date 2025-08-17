import pygame

from dung.settings import *
from dung.size_settings import SIZES
from dung.font_settings import FONTS


def draw_header_section(screen):
    rect = pygame.Rect(0, 0, SIZES.WIDTH + SIZES.SIDEBAR_SECTION_SIZE, SIZES.HEADER_SECTION_SIZE)
    pygame.draw.rect(screen, GRAY, rect)
    pygame.draw.rect(screen, BLACK, rect, width=3)

    title_text = GAME_NAME
    title_width, title_height = FONTS.LARGE_FONT.size(title_text)
    label = FONTS.LARGE_FONT.render(title_text, True, BLACK)
    screen.blit(label, (((SIZES.WIDTH + SIZES.SIDEBAR_SECTION_SIZE) - title_width) // 2, (SIZES.HEADER_SECTION_SIZE - title_height) // 2))
