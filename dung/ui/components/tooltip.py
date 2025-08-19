import pygame

from dung.settings import *


class Tooltip:
    def __init__(self):
        self.bg_color = WHITE
        self.border_color = BLACK
        self.padding = (4, 3)  # (horizontal, vertical)
        self.border_radius = 2

    def draw(self, surface, font, text, position, direction="topleft",header=None, header_font=None, max_width=None, max_height=None, space_before_footer=False, footer=None):
        text_surfaces = []
        if header:
            header_lines = self._wrap_text(font, header, max_width) if max_width else [header]
            for line in header_lines:
                text_surfaces.append((header_font or font).render(line, True, (0, 0, 0)) )

        text_lines = self._wrap_text(font, text, max_width) if max_width else [text]
        total_lines = len(text_lines)
        for line in text_lines:
            text_surfaces.append(font.render(line, True, (0, 0, 0)))

        if footer is not None:
            if space_before_footer:
                text_surfaces.append(font.render("", True, (0, 0, 0)))
                total_lines += 1
                
            footer_lines = self._wrap_text(font, footer, max_width) if max_width else [footer]
            for line in footer_lines:
                text_surfaces.append(font.render(line, True, (0, 0, 0)))
            total_lines += len(footer_lines)

        header_line_height = (header_font or font).get_height()
        text_line_height = font.get_height()
        total_text_height = header_line_height * len(header_lines) + text_line_height * total_lines
        max_line_width = max(s.get_width() for s in text_surfaces)

        # Clip height if needed
        if max_height and total_text_height > max_height:
            visible_lines = 0
            calculated_height = 0
            for i in enumerate(header_lines):
                calculated_height += header_line_height
                if calculated_height <= max_height:
                    visible_lines += 1
                else:
                    break

            if calculated_height < max_height:
                for i in enumerate(text_lines):
                    calculated_height += text_line_height
                    if calculated_height <= max_height:
                        visible_lines += 1 
                    else:
                        break

            visible_lines = text_surfaces[:visible_lines]

        # Calculate tooltip box size
        bg_width = max_line_width + self.padding[0] * 2
        bg_height = total_text_height + self.padding[1] * 2
        bg_rect = pygame.Rect(0, 0, bg_width, bg_height)

        # Align based on direction
        setattr(bg_rect, direction, position)

        # Draw background and border
        pygame.draw.rect(surface, self.bg_color, bg_rect, border_radius=self.border_radius)
        pygame.draw.rect(surface, self.border_color, bg_rect, width=1, border_radius=self.border_radius)

        # Draw each line of text
        x = bg_rect.x + self.padding[0]
        y = bg_rect.y + self.padding[1]
        for surf in text_surfaces:
            surface.blit(surf, (x, y))
            y += surf.get_height()

    def _wrap_text(self, font, text, max_width):
        """Splits the text into lines so that each fits within max_width."""
        words = text.split(' ')
        lines = []
        current_line = ""

        for word in words:
            test_line = f"{current_line} {word}".strip()
            width = font.size(test_line)[0]
            if width <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word

        if current_line:
            lines.append(current_line)

        return lines
