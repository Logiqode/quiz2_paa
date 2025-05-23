import pygame
from settings import GRID_SIZE, GRID_COLS, GRID_ROWS, KEYBINDS
from core.algorithms.pathfinder import Pathfinder

class InputHandler:
    def __init__(self, game):
        self.game = game

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.handle_mouse_click(event)
        elif event.type == pygame.KEYDOWN:
            self.handle_key_press(event)

    def handle_mouse_click(self, event):
        if event.button == 1:  # Left click
            mouse_x, mouse_y = pygame.mouse.get_pos()
            grid_x, grid_y = mouse_x // GRID_SIZE, mouse_y // GRID_SIZE
            
            if 0 <= grid_x < GRID_COLS and 0 <= grid_y < GRID_ROWS:
                if self.game.state.grid[grid_y][grid_x] == 0:  # Walkable
                    self.game.state.target_pos = (grid_x, grid_y)
                    #Change Algorithms to your liking
                    self.game.state.path = self.game.pathfinder.bfs(
                        self.game.state.player_grid_pos,
                        self.game.state.target_pos,
                        self.game.state.grid
                    )
                    self.game.state.is_moving = False

    def handle_key_press(self, event):
        if event.key == KEYBINDS["quit"]:
            self.game.quit_game()
        elif event.key == KEYBINDS["reset"]:
            self.game.state.reset()