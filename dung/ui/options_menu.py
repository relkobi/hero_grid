import pygame

from dung.settings import *
from dung.size_settings import SIZES
from dung.font_settings import FONTS

def _render_options_menu_button(screen, event_list, item, x: int, y: int):
    mouse_pos = pygame.mouse.get_pos()
    font = FONTS.MEDUIM_FONT

    label = font.render(item, True, BLACK)
    text_rect = label.get_rect(center=(x, y))
    
    rect = pygame.Rect(x, y, 600, 60)
    rect.center = (x, y)
    # Brighten color on hover
    if rect.collidepoint(mouse_pos):
        color = YELLOW
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pygame.event.post(pygame.event.Event(OPTIONS_MENU_ITEM_CLICKED, {"item": item}))
    else:
        color = WHITE

    pygame.draw.rect(screen, color, rect, border_radius=2)
    pygame.draw.rect(screen, BLACK, rect, border_radius=2, width=1)

    screen.blit(label, text_rect)

    return rect

def draw_options_menu(screen, event_list):
    # Overlay
    overlay = pygame.Surface((SIZES.WIDTH + SIZES.SIDEBAR_SECTION_SIZE, SIZES.HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))  # RGBA: 150 is opacity (0 = transparent, 255 = opaque)
    screen.blit(overlay, (0, SIZES.HEADER_SECTION_SIZE))

    # Popup Frame
    x_center = int(screen.get_width() // 2)
    options_rect = pygame.Rect(0, 0, 800, 600)
    options_rect.center = (x_center, (screen.get_height() - SIZES.HEADER_SECTION_SIZE) // 2 + SIZES.HEADER_SECTION_SIZE)

    pygame.draw.rect(screen, WHITE, options_rect, border_radius=10)
    pygame.draw.rect(screen, BLACK, options_rect, border_radius=10, width=5)

    y_offset = options_rect.y + FONTS.LARGE_FONT.get_height() // 2 + 10

    # Title    
    title_label = FONTS.LARGE_FONT.render("OPTIONS MENU", True, BLACK)
    title_rect = title_label.get_rect(center=(x_center, y_offset))
    screen.blit(title_label, title_rect)
    y_offset += FONTS.LARGE_FONT.get_height() * 1.5

    # Items
    menu_items = [OM_NEW_RUN_ITEM, OM_MAIN_MENU_ITEM, OM_SETTINGS_ITEM, OM_EXIT_GAME_ITEM]
    for item in menu_items:
        item_rect = _render_options_menu_button(screen, event_list, item, x_center, y_offset)
        y_offset += item_rect.height * 1.5
  
