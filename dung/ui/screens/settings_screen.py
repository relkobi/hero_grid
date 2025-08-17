from dung.ui.components.settings_items import draw_settings_items
from dung.settings import *
from dung.size_settings import SIZES
from dung.ui.components.titled_grid import draw_titled_grid


def draw_settings_screen(screen, event_list):
    x_center = int(screen.get_width() // 2)
    y_offset = int(screen.get_height() * 0.35)

    draw_titled_grid(screen)
    draw_settings_items(screen, event_list, x_center, y_offset)