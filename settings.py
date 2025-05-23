import pygame

# Game settings
TITLE = "Pathfinding Game"
WIDTH = 800
HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GRAY = (160, 160, 160)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BROWN = (139, 69, 19)
YELLOW = (255, 255, 0)

# Grid settings
GRID_SIZE = 20
GRID_COLS = WIDTH // GRID_SIZE
GRID_ROWS = HEIGHT // GRID_SIZE

# Keybinds
KEYBINDS = {
    "quit": pygame.K_ESCAPE,
    "reset": pygame.K_r,
    "toggle_obstacle": pygame.K_o
}