import pygame
from dung.settings import BLACK, GRAY, WHITE
from dung.font_settings import FONTS
from dung.utils import wrap_text

class BattleLog:
    def __init__(self, x, y, width, visible_lines):
        self.x = x
        self.y = y
        self.width = width
        self.visible_lines = visible_lines
        self.font = FONTS.TEXT_FONT
        self.text_color = BLACK
        self.bg_color = WHITE
        self.border_color = BLACK

        self.line_height = self.font.get_height()
        self.height = self.visible_lines * self.line_height
        self.rect = pygame.Rect(x, y, width, self.height)

        self.messages = []
        self.scroll_offset = 0
        self.user_scrolled_up = False

    def add_message(self, logs, color=None):
        messages = wrap_text(logs, self.font, self.width)
        for message in messages:
            self.messages.append((message, color or self.text_color))
        max_scroll = max(0, len(self.messages) - self.visible_lines)

        # Always jump to latest message when a new message arrives
        self.scroll_offset = max_scroll
        self.user_scrolled_up = False


    def clear(self):
        self.messages.clear()
        self.scroll_offset = 0
        self.user_scrolled_up = False


    def scroll_up(self):
        if self.scroll_offset > 0:
            self.scroll_offset -= 1
            self.user_scrolled_up = True

    def scroll_down(self):
        max_scroll = max(0, len(self.messages) - self.visible_lines)
        if self.scroll_offset < max_scroll:
            self.scroll_offset += 1
            if self.scroll_offset == max_scroll:
                self.user_scrolled_up = False

    def draw(self, surface):
        # Draw background and border
        pygame.draw.rect(surface, self.bg_color, self.rect)
        pygame.draw.rect(surface, self.border_color, self.rect, 2)

        # Get visible messages
        max_scroll = max(0, len(self.messages) - self.visible_lines)
        self.scroll_offset = max(0, min(self.scroll_offset, max_scroll))
        visible = self.messages[self.scroll_offset:self.scroll_offset + self.visible_lines]

        last_index = len(self.messages) - 1
        # for i, (text, color) in enumerate(visible):
        #     rendered = self.font.render(text, True, color)
        #     surface.blit(rendered, (self.rect.x + 5, self.rect.y + i * self.line_height))

        for i, (text, _) in enumerate(visible):
            global_index = self.scroll_offset + i
            # Use black for the last message, gray for others
            color = BLACK if global_index == last_index else GRAY
            rendered = self.font.render(text, True, color)
            surface.blit(rendered, (self.rect.x + 5, self.rect.y + i * self.line_height))
