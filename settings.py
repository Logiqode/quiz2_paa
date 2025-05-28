# settings.py
import pygame

TITLE = "Pathfinding Game"
WIDTH = 800
HEIGHT = 600
FPS = 60

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GRAY = (160, 160, 160)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BROWN = (139, 69, 19)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
LIGHT_GRAY = (211, 211, 211)
DEFAULT_COLOR = WHITE

GRID_SIZE = 16
GRID_COLS = WIDTH // GRID_SIZE
GRID_ROWS = HEIGHT // GRID_SIZE

KEYBINDS = {
    "quit": pygame.K_ESCAPE,
    "reset": pygame.K_r,
    "toggle_obstacle": pygame.K_o,
    "human": pygame.K_1,
    "bat": pygame.K_2,
    "rat": pygame.K_3,
}

FORM_COLORS = {
    'human': GREEN,
    'bat': PURPLE,
    'rat': LIGHT_GRAY,
}

BAT_SPRITESHEET_PATH = "assets/sprites/32x32-bat-sprite_4.png"
BAT_ANIMATION_SPEED = 0.1
BAT_SPRITE_NATIVE_WIDTH = 32
BAT_SPRITE_NATIVE_HEIGHT = 32
BAT_FLAP_FRAMES_COUNT = 4

HUMAN_SPRITESHEET_PATH = "assets/sprites/acolyte_human.png"
HUMAN_ANIMATION_SPEED = 0.15
HUMAN_SPRITE_NATIVE_WIDTH = 32 
HUMAN_SPRITE_NATIVE_HEIGHT = 32

HUMAN_WALK_DOWN_FRAMES_COUNT = 2 
HUMAN_WALK_UP_FRAMES_COUNT = 2
HUMAN_WALK_RIGHT_FRAMES_COUNT = 3

HUMAN_ANIMATION_OFFSETS = {
    "walk_down": (0, 0),
    "walk_up": (0, 2),
    "walk_right": (1, 0)
}

RAT_SPRITESHEET_PATH = "assets/sprites/lpccatratdog.png"
RAT_ANIMATION_SPEED = 0.1
RAT_SPRITE_NATIVE_WIDTH = 32
RAT_SPRITE_NATIVE_HEIGHT = 32
RAT_ANIMATION_FRAMES_PER_DIRECTION = 3

RAT_ANIMATION_ROW_OFFSETS = {
    "up": 3,
    "left": 1,
    "right": 2,
    "down": 0,
}
