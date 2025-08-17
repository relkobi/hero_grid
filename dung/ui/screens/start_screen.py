
import pygame

from dung.settings import *
from dung.size_settings import SIZES
from dung.font_settings import FONTS
from dung.ui.components.titled_grid import draw_titled_grid

def get_base_width():
    return max(SIZES.SCREEN_WIDTH * 0.4, 600)

def get_base_height():
    return max(FONTS.MEDUIM_FONT.get_height() * 1.4, 60)

def _render_start_screen_button(screen, event_list, item, x: int, y: int):
    mouse_pos = pygame.mouse.get_pos()
    font = FONTS.MEDUIM_FONT

    label = font.render(item, True, BLACK)
    text_rect = label.get_rect(center=(x, y))
    
    rect = pygame.Rect(x, y, get_base_width(), get_base_height())
    rect.center = (x, y)
    # Brighten color on hover
    if rect.collidepoint(mouse_pos):
        color = YELLOW
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pygame.event.post(pygame.event.Event(START_SCREEN_ITEM_CLICKED, {"item": item}))
    else:
        color = WHITE

    pygame.draw.rect(screen, color, rect, border_radius=2)
    pygame.draw.rect(screen, BLACK, rect, border_radius=2, width=1)

    screen.blit(label, text_rect)

def draw_start_screen(screen, event_list):
    x_center = SIZES.SCREEN_WIDTH // 2
    y_offset = SIZES.SCREEN_HEIGHT * 0.15

    draw_titled_grid(screen)

    y_offset += SIZES.SCREEN_HEIGHT * 0.3

    menu_items = [SS_START_GAME_ITEM, SS_COMPENDIUM_ITEM, SS_SETTINGS_ITEM, SS_CREDITS_ITEM, SS_EXIT_GAME_ITEM]
    for item in menu_items:
        _render_start_screen_button(screen, event_list, item, x_center, y_offset)
        y_offset += int(get_base_height() * 1.2)