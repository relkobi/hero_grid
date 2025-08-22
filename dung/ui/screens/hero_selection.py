import pygame

from dung.utils import wrap_text
from dung.settings import *
from dung.monster_settings import * 
from dung.size_settings import SIZES
from dung.font_settings import FONTS

def _show_text(screen, font, text, y_offset):
    label = font.render(text, True, BLACK)
    rect = label.get_rect(center=(SIZES.SCREEN_WIDTH // 2, y_offset))
    screen.blit(label, rect)

def draw_hero_selection_screen(screen, event_list):
    mouse_pos = pygame.mouse.get_pos()

    _show_text(screen, FONTS.LARGE_FONT, "Choose Your Hero", y_offset=SIZES.SCREEN_WIDTH * 0.05)

    heroes = HEROES_SETTINGS.keys()

    hero_units = 3
    margin_units = 1
    total_units = len(heroes) * hero_units + (len(heroes) + 1) * margin_units
    unit_size = SIZES.SCREEN_WIDTH // total_units
    x_offset = unit_size
    for i, hero_name in enumerate(heroes):
        hero_settings = HEROES_SETTINGS[hero_name]
        hero_active = hero_settings["is-active"]
        hero_size = unit_size * hero_units
        hero_margin = unit_size
        hero_rect = pygame.Rect(x_offset + i * (hero_size + hero_margin), round(SIZES.SCREEN_WIDTH * 0.15), hero_size, hero_size)

        hero_title = hero_name.capitalize()
        text_width, text_height = FONTS.TITLE_FONT.size(hero_title)
        label = FONTS.TITLE_FONT.render(hero_title, True, BLACK)
        screen.blit(label, (hero_rect.x + (hero_size - text_width) // 2, hero_rect.y + hero_size + 10))

        hero_info = False
        if hero_active and hero_rect.collidepoint(mouse_pos):
            color = YELLOW
            frame_width = 3
            for event in event_list:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    pygame.event.post(pygame.event.Event(HERO_SELECTION_HERO_CLICKED, {"hero": hero_name}))
            hero_info = True
        else:
            color = WHITE
            frame_width = 2


        pygame.draw.rect(screen, color, hero_rect)

        hero_image = pygame.image.load(resource_path(f"dung/assets/images/{hero_name.lower()}.png"))
        hero_image = pygame.transform.scale(hero_image, (hero_size, hero_size))

        if (not hero_active):
            hero_image = hero_image.convert_alpha()
            for x in range(hero_image.get_width()):
                for y in range(hero_image.get_height()):
                    r, g, b, a = hero_image.get_at((x, y))

                    if a == 0:
                        # Fully transparent: make it white and fully transparent
                        hero_image.set_at((x, y), (255, 255, 255, 0))
                    else:
                        # Convert to grayscale
                        gray = int(0.299 * r + 0.587 * g + 0.114 * b)
                        hero_image.set_at((x, y), (gray, gray, gray, a))

            screen.blit(hero_image, hero_rect)

            in_progress_title = "In Progress"
            in_progress_width, in_progress_height = FONTS.TITLE_FONT.size(in_progress_title)
            in_progress_label = FONTS.TITLE_FONT.render(in_progress_title, True, YELLOW)
            screen.blit(in_progress_label, (hero_rect.x + (hero_size - in_progress_width) // 2, hero_rect.y + hero_size // 2))
        else:
            screen.blit(hero_image, hero_rect)

        pygame.draw.rect(screen, BLACK, hero_rect, width=frame_width)

        if hero_info:
            info_width = len(heroes) * (hero_size + hero_margin) - hero_margin
            info_rect = pygame.Rect(x_offset , hero_rect.y + hero_size + text_height + 50, info_width, hero_size // 2)
            pygame.draw.rect(screen, WHITE, info_rect)
            
            info_font = FONTS.TEXT_FONT
            lines = wrap_text(hero_settings["info"], info_font, info_width - 20)
            line_height = info_font.get_height() + 10
            for i, line in enumerate(lines):
                label = info_font.render(line, True, BLACK)
                screen.blit(label, (info_rect.x + 10, info_rect.y + 10 + (i * line_height)))
