import pygame

from dung import game_settings
from dung.font_settings import FONTS
from dung.game_settings import game_settings
from dung.settings import *
from dung.size_settings import SIZES
from dung.ui.components.volume_slider import VolumeSlider

volume_slider = None

def get_base_width():
    return max(SIZES.SCREEN_WIDTH * 0.4, 600)

def get_base_height():
    return max(FONTS.MEDUIM_FONT.get_height() * 1.4, 60)

def _render_triangle_switch_button(
    screen,
    event_list,
    options: list[dict],
    selected_index: int,
    publish_event,
    x: int,
    y: int,
) -> pygame.Rect:
    current_option = options[selected_index]
    text = current_option["label"]

    mouse_pos = pygame.mouse.get_pos()
    font = FONTS.MEDUIM_FONT

    label = font.render(text, True, BLACK)
    text_rect = label.get_rect(center=(x, y))

    rect_width, rect_height = get_base_width(), get_base_height()
    rect = pygame.Rect(0, 0, rect_width, rect_height)
    rect.center = (x, y)

    triangle_margin = 10
    triangle_width = 20
    triangle_height = int(rect_height * 0.8)

    top_y = y - triangle_height // 2
    bottom_y = y + triangle_height // 2

    left_tip_x = rect.left - triangle_margin - triangle_width
    left_triangle = [
        (left_tip_x, y),
        (left_tip_x + triangle_width, top_y),
        (left_tip_x + triangle_width, bottom_y),
    ]
    left_click_area = pygame.Rect(left_tip_x, top_y, triangle_width, triangle_height)

    right_tip_x = rect.right + triangle_margin + triangle_width
    right_triangle = [
        (right_tip_x, y),
        (right_tip_x - triangle_width, top_y),
        (right_tip_x - triangle_width, bottom_y),
    ]
    right_click_area = pygame.Rect(right_tip_x - triangle_width, top_y, triangle_width, triangle_height)

    hover_left = left_click_area.collidepoint(mouse_pos)
    hover_right = right_click_area.collidepoint(mouse_pos)

    new_index = None
    for event in event_list:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if hover_left:
                new_index = (selected_index - 1) % len(options)
            elif hover_right:
                new_index = (selected_index + 1) % len(options)

    pygame.draw.rect(screen, WHITE, rect, border_radius=2)
    pygame.draw.rect(screen, BLACK, rect, border_radius=2, width=1)
    screen.blit(label, text_rect)

    pygame.draw.polygon(screen, YELLOW if hover_left else BLACK, left_triangle)
    pygame.draw.polygon(screen, YELLOW if hover_right else BLACK, right_triangle)

    if new_index is not None:
        pygame.event.post(pygame.event.Event(publish_event, options[new_index]["event_data"]))


    return rect, new_index is not None


def _render_settings_menu_button(screen, event_list, text, publish_event, event_data,  x: int, y: int):
    mouse_pos = pygame.mouse.get_pos()
    font = FONTS.MEDUIM_FONT

    label = font.render(text, True, BLACK)
    text_rect = label.get_rect(center=(x, y))
    
    rect = pygame.Rect(x, y, get_base_width(), get_base_height())
    rect.center = (x, y)
    # Brighten color on hover
    if rect.collidepoint(mouse_pos):
        color = YELLOW
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pygame.event.post(pygame.event.Event(publish_event, event_data))
    else:
        color = WHITE

    pygame.draw.rect(screen, color, rect, border_radius=2)
    pygame.draw.rect(screen, BLACK, rect, border_radius=2, width=1)

    screen.blit(label, text_rect)

    return rect

def draw_settings_items(screen, event_list, x_center, y_start):
    y_offset = y_start
    # Title    
    title_label = FONTS.LARGE_FONT.render("SETTINGS", True, BLACK)
    title_rect = title_label.get_rect(center=(x_center, y_offset))
    screen.blit(title_label, title_rect)
    y_offset += FONTS.LARGE_FONT.get_height() * 1.2

    # View Mode
    view_mode_rect, _ =_render_triangle_switch_button(
        screen,
        event_list,
        [{"label": "Fullscreen", "event_data": {"fullscreen": True}}, {"label": "Windowed", "event_data": {"fullscreen": False}}],
        0 if game_settings.fullscreen is True else 1,
        SETTINGS_MENU_FULLSCREEN,
        x_center,
        y_offset,
    )
    y_offset += view_mode_rect.height * 1.2

    # Resolutions
    resolutions = [  
        {"label": "1024 x 768", "event_data": {"resolution": [1024, 768]}},
        {"label": "1280 x 720", "event_data": {"resolution": [1280, 720]}}, 
        {"label": "1920 x 1080", "event_data": {"resolution": [1920, 1080]}}, 
        {"label": "2560 x 1440", "event_data": {"resolution": [2560, 1440]}}, 
    ]
    selected_resolution_index = next(i for i, r in enumerate(resolutions) if r["event_data"]["resolution"] == game_settings.resolution)
    resolution_rect, resolution_changed =_render_triangle_switch_button(
        screen,
        event_list,
        resolutions,
        selected_resolution_index,
        SETTINGS_MENU_SET_RESOLUTION,
        x_center,
        y_offset,
    )
    y_offset += resolution_rect.height * 1.2

    # Sound Toggle    
    sound_text = f"Turn Sound {"Off" if game_settings.sound is True else "On"}"
    sound_event_data = { "sound": not game_settings.sound}
    item_rect = _render_settings_menu_button(screen, event_list, sound_text, SETTINGS_MENU_TOGGLE_SOUND, sound_event_data, x_center, y_offset)
    y_offset += item_rect.height * 1.2

    # Volume mixer
    y_offset += item_rect.height * 0.5
    global volume_slider
    if volume_slider:
        if volume_slider.dirty:
            volume_slider.resize(x_center, y_offset, get_base_width(), FONTS.MEDUIM_FONT)
            volume_slider.dirty = False
        volume_slider.update_volume(game_settings.volume, False)
    else:
        volume_slider = VolumeSlider(x_center, y_offset, get_base_width(), FONTS.MEDUIM_FONT, event_type=SETTINGS_MENU_SET_SOUND_VOLUME, initial_volume=game_settings.volume)

    if resolution_changed:
        volume_slider.dirty = True # update to true after the check so the state will be checked on next draw call so x,y will get updated

    volume_slider.draw(screen)
    for event in event_list:
        volume_slider.handle_event(event)
    y_offset += item_rect.height

    # Back Button as Footer
    # back_y = y_start + get_base_width() - item_rect.height
    item_rect = _render_settings_menu_button(screen, event_list, "Back", SETTINGS_MENU_BACK, {}, x_center, y_offset)
    