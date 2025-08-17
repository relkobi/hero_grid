import pygame

from dung.font_settings import FONTS
from dung.settings import *
from dung.size_settings import SIZES


def _draw_grid(screen):
    grid_size = int(SIZES.SCREEN_HEIGHT * 0.1)
    x = grid_size // 2
    y = grid_size // 2
    width = SIZES.SCREEN_WIDTH - grid_size
    height = grid_size * 3

    # Vertical Lines
    for xx in range(x + grid_size // 2, x + width, grid_size):
        pygame.draw.line(screen, GRAY, (xx, y), (xx, y + height), width=2)
    # Horizontal Lines
    for yy in range(y + grid_size // 2, y + height, grid_size):
        pygame.draw.line(screen, GRAY, (x, yy), (x + width, yy), width=2)

def _render_menu_title(screen, font, color, text, x, y):

    label = font.render(text, True, color)
    rect = label.get_rect(center=(x, y))

    screen.blit(label, rect)

def _render_start_screen_button(screen, event_list, item, x: int, y: int):
    mouse_pos = pygame.mouse.get_pos()
    font = FONTS.MEDUIM_FONT

    label = font.render(item, True, BLACK)
    text_rect = label.get_rect(center=(x, y))
    
    rect = pygame.Rect(x, y, SIZES.SCREEN_WIDTH * 0.5, SIZES.SCREEN_HEIGHT * 0.08)
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

def draw_titled_grid(screen):
    x_center = SIZES.SCREEN_WIDTH // 2
    y_offset = SIZES.SCREEN_HEIGHT * 0.2

    _draw_grid(screen)
    _render_menu_title(screen, FONTS.START_FONT, BLACK, GAME_NAME, x_center, y_offset)
