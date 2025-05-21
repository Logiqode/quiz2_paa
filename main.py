import pygame
from game.player.movement.controller import handle_mouse_click, get_reachable_area
from game.keybinds.loader import load_keybinds
from data.map.mansion_floor_1 import TILE_MAP
from data.colors import *

# Constants
GRID_WIDTH, GRID_HEIGHT = 10, 10
TILE_SIZE = 48
player_pos = {"x": 0, "y": 0}
reachable_area = [get_reachable_area(player_pos["x"], player_pos["y"], TILE_MAP)]  # mutable list
keybinds = load_keybinds()

# Init Pygame
pygame.init()
screen = pygame.display.set_mode((GRID_WIDTH * TILE_SIZE, GRID_HEIGHT * TILE_SIZE))
pygame.display.set_caption("Top-Down Grid Map")


def draw_grid():
    screen.fill(BLACK)
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            tile = TILE_MAP[y, x]
            if tile == 1:      # Wall
                color = GRAY
            elif tile == 2:    # Obstacle
                color = YELLOW
            elif tile == 3:    # Container
                color = GREEN
            elif tile == 4:    # Ladder
                color = BROWN
            elif tile == 0:    # Walkable
                color = WHITE
            else:
                color = BLACK

            rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, BLACK, rect, 1)

    px, py = player_pos["x"], player_pos["y"]
    center = (px * TILE_SIZE + TILE_SIZE // 2, py * TILE_SIZE + TILE_SIZE // 2)
    pygame.draw.circle(screen, BLUE, center, TILE_SIZE // 3)
    pygame.display.flip()


# Main loop
running = True
clock = pygame.time.Clock()

while running:
    draw_grid()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            handle_mouse_click(event, player_pos, TILE_MAP, TILE_SIZE, reachable_area)

        elif event.type == pygame.KEYDOWN:
            if event.key == keybinds["use"]:
                px, py = player_pos["x"], player_pos["y"]
                tile = TILE_MAP[py, px]
                if tile == 3:
                    print("Open container")
                elif tile == 4:
                    print("Interact with ladder")
                elif tile == 2:
                    print("Obstacle interaction logic")

    clock.tick(60)

pygame.quit()
