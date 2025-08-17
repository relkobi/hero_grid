import pygame

from dung.ui.components.volume_slider import VolumeSlider
from dung.settings import *
from dung.game_settings import game_settings
from dung.size_settings import SIZES
from dung.font_settings import FONTS

volume_slider = None

def _render_settings_menu_button(screen, event_list, text, publish_event, event_data,  x: int, y: int):
    mouse_pos = pygame.mouse.get_pos()
    font = FONTS.MEDUIM_FONT

    label = font.render(text, True, BLACK)
    text_rect = label.get_rect(center=(x, y))
    
    rect = pygame.Rect(x, y, 600, 60)
    rect.center = (x, y)
    # Brighten color on hover
    if rect.collidepoint(mouse_pos):
        color = YELLOW
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                print("publish_event", event_data)
                pygame.event.post(pygame.event.Event(publish_event, event_data))
    else:
        color = WHITE

    pygame.draw.rect(screen, color, rect, border_radius=2)
    pygame.draw.rect(screen, BLACK, rect, border_radius=2, width=1)

    screen.blit(label, text_rect)

    return rect

def draw_settings_menu(screen, event_list):
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
    title_label = FONTS.LARGE_FONT.render("SETTINGS MENU", True, BLACK)
    title_rect = title_label.get_rect(center=(x_center, y_offset))
    screen.blit(title_label, title_rect)
    y_offset += FONTS.LARGE_FONT.get_height() * 1.2

    # View Mode    
    view_mode_text = f"{"Fullscreen" if game_settings.fullscreen is True else "Windowed"}"
    view_mode_event_data = { "fullscreen": not game_settings.fullscreen}
    item_rect = _render_settings_menu_button(screen, event_list, view_mode_text, SETTINGS_MENU_FULLSCREEN, view_mode_event_data, x_center, y_offset)
    y_offset += item_rect.height * 1.5

    # Sound Toggle    
    sound_text = f"Turn Sound {"Off" if game_settings.sound is True else "On"}"
    sound_event_data = { "sound": not game_settings.sound}
    item_rect = _render_settings_menu_button(screen, event_list, sound_text, SETTINGS_MENU_TOGGLE_SOUND, sound_event_data, x_center, y_offset)
    y_offset += item_rect.height * 1.5
  
    # Volume mixer
    y_offset += item_rect.height * 0.5
    global volume_slider
    if volume_slider:
        volume_slider.update_volume(game_settings.volume, False)
    else:
        volume_slider = VolumeSlider(x_center, y_offset, 600, FONTS.MEDUIM_FONT, event_type=SETTINGS_MENU_SET_SOUND_VOLUME, initial_volume=game_settings.volume)

    volume_slider.draw(screen)
    for event in event_list:
        volume_slider.handle_event(event)
    y_offset += item_rect.height * 1.5


    # Back Button as Footer
    back_y = options_rect.y + 600 - item_rect.height
    item_rect = _render_settings_menu_button(screen, event_list, "Back", SETTINGS_MENU_BACK, {}, x_center, back_y)

