import pygame
import math

def draw_square_pie(screen, rect, percent, color):
    if percent <= 0:
        return
    if percent >= 100:
        pygame.draw.rect(screen, color, rect)
        return

    center = (rect.width / 2, rect.height / 2)
    w, h = rect.width, rect.height

    # Perimeter of the square path we use (start at top center, go clockwise):
    # The path is 4 edges: top-center -> top-right -> bottom-right -> bottom-left -> top-left -> top-center
    # We define these 5 points (the path is closed)
    path_points = [
        (w/2, 0),        # top center
        (w, 0),          # top-right corner
        (w, h),          # bottom-right corner
        (0, h),          # bottom-left corner
        (0, 0),          # top-left corner
        (w/2, 0)         # back to top center to close loop
    ]

    # Compute total perimeter length of the path (sum of segments)
    def dist(p1, p2):
        return math.hypot(p2[0]-p1[0], p2[1]-p1[1])
    perimeter = 0
    for i in range(len(path_points)-1):
        perimeter += dist(path_points[i], path_points[i+1])

    target_length = (percent / 100) * perimeter

    points = [center]  # start polygon from center
    length_accum = 0

    # Walk along path_points edges accumulating length until target_length reached
    for i in range(len(path_points) - 1):
        start = path_points[i]
        end = path_points[i + 1]
        edge_len = dist(start, end)

        if length_accum + edge_len >= target_length:
            remain = target_length - length_accum
            ratio = remain / edge_len
            interp_x = start[0] + (end[0] - start[0]) * ratio
            interp_y = start[1] + (end[1] - start[1]) * ratio
            points.append(start)
            points.append((interp_x, interp_y))
            break
        else:
            points.append(start)
            length_accum += edge_len

    # Draw polygon on transparent surface and blit it
    pie_surface = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.draw.polygon(pie_surface, color, points)
    screen.blit(pie_surface, rect.topleft)

pygame.init()
screen = pygame.display.set_mode((400, 400))
clock = pygame.time.Clock()

rect = pygame.Rect(100, 100, 200, 200)
color = (255, 100, 100)
percent = 0

running = True
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

    screen.fill((30, 30, 30))
    draw_square_pie(screen, rect, percent, color)
    pygame.draw.rect(screen, (200, 200, 200), rect, 2)

    percent += 0.5
    if percent > 100:
        percent = 0

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
