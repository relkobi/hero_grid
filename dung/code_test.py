import pygame
import random

pygame.init()
screen = pygame.display.set_mode((640, 640))
clock = pygame.time.Clock()

width, height = 20, 20
TILE_SIZE = 32

world = [[1 for _ in range(width)] for _ in range(height)]

def generate_cave(world, steps=200):
    x, y = width // 2, height // 2
    world[y][x] = 0
    for _ in range(steps):
        dx, dy = random.choice([(0,1), (1,0), (0,-1), (-1,0)])
        x = max(1, min(x + dx, width - 2))
        y = max(1, min(y + dy, height - 2))
        world[y][x] = 0

def draw_world(screen, world):
    for y in range(height):
        for x in range(width):
            color = (30, 30, 30) if world[y][x] == 1 else (200, 200, 200)
            pygame.draw.rect(
                screen, color, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            )

    # Draw grid lines
    for x in range(width + 1):
        pygame.draw.line(screen, (100, 100, 100), (x * TILE_SIZE, 0), (x * TILE_SIZE, height * TILE_SIZE))
    for y in range(height + 1):
        pygame.draw.line(screen, (100, 100, 100), (0, y * TILE_SIZE), (width * TILE_SIZE, y * TILE_SIZE))


generate_cave(world)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))
    draw_world(screen, world)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
