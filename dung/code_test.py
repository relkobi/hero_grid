import pygame
import math

pygame.init()
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Accurate Square Pie Chart")

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 120, 255)
DARK_BLUE = (0, 80, 180)

# Square setup
rect = pygame.Rect(100, 80, 150, 150)
percentage = 123
  # Target fill % (0 to 100)

def draw_square_pie(surface, rect, percent, color):
    if percent <= 0:
        return  # Nothing to draw

    # Create a surface to draw on
    pie_surface = pygame.Surface(rect.size, pygame.SRCALPHA)

    center = (rect.width // 2, rect.height // 2)
    total_area = rect.width * rect.height
    target_area = (percent / 100) * total_area

    # Parameters
    num_steps = 360  # More = smoother pie
    step_angle = 2 * math.pi / num_steps
    current_area = 0
    points = [center]

    # Start drawing sectors until we hit the desired area
    for i in range(num_steps + 1):
        angle = i * step_angle
        x = center[0] + rect.width * math.cos(angle - math.pi / 2)
        y = center[1] + rect.height * math.sin(angle - math.pi / 2)

        x = max(0, min(rect.width, x))
        y = max(0, min(rect.height, y))

        if i > 0:
            # Estimate triangle area between center and two points
            ax, ay = points[-1]
            bx, by = x, y
            tri_area = 0.5 * abs((ax - center[0]) * (by - center[1]) - (bx - center[0]) * (ay - center[1]))
            current_area += tri_area

            if current_area >= target_area:
                break

        points.append((x, y))

    if len(points) > 2:
        pygame.draw.polygon(pie_surface, color, points)
        surface.blit(pie_surface, rect.topleft)


# Main loop
running = True
while running:
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLUE, rect)  # Draw base square

    draw_square_pie(screen, rect, percentage, DARK_BLUE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

pygame.quit()
