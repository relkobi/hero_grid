from pydoc import text
import pygame
from dung.font_settings import FONTS


mouse_pos = pygame.mouse.get_pos()
font = FONTS.MEDUIM_FONT

label = font.render(text, True, BLACK)
text_rect = label.get_rect(center=(x, y))

# Main button rectangle
rect = pygame.Rect(0, 0, 600, 60)
rect.center = (x, y)

# Triangle size and position offsets
triangle_size = 20
spacing = 20

# LEFT triangle (◄)
left_triangle = [
    (x - rect.width // 2 - spacing, y),                         # tip
    (x - rect.width // 2 - spacing + triangle_size, y - 10),    # top
    (x - rect.width // 2 - spacing + triangle_size, y + 10),    # bottom
]

# RIGHT triangle (►)
right_triangle = [
    (x + rect.width // 2 + spacing, y),                         # tip
    (x + rect.width // 2 + spacing - triangle_size, y - 10),    # top
    (x + rect.width // 2 + spacing - triangle_size, y + 10),    # bottom
]

# Create small Rects for click detection
left_click_area = pygame.Rect(
    x - rect.width // 2 - spacing, y - 10, triangle_size, 20
)
right_click_area = pygame.Rect(
    x + rect.width // 2 + spacing - triangle_size, y - 10, triangle_size, 20
)

# Color changes on hover
if rect.collidepoint(mouse_pos):
    color = YELLOW
else:
    color = WHITE

# Check triangle clicks
for event in event_list:
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        if left_click_area.collidepoint(mouse_pos):
            print("Left triangle clicked — previous option")
            # You can replace this with an actual event trigger
        elif right_click_area.collidepoint(mouse_pos):
            print("Right triangle clicked — next option")
            # Same here for event trigger
        elif rect.collidepoint(mouse_pos):
            print("Center button clicked")
            pygame.event.post(pygame.event.Event(publish_event, event_data))

# Draw everything
pygame.draw.rect(screen, color, rect, border_radius=2)
pygame.draw.rect(screen, BLACK, rect, border_radius=2, width=1)
screen.blit(label, text_rect)

# Draw triangles
pygame.draw.polygon(screen, BLACK, left_triangle)
pygame.draw.polygon(screen, BLACK, right_triangle)
