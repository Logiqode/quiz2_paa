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
            # Get scale factor from game
            scale_factor = self.game.scale_factor
            
            # Scale mouse coordinates back to original size
            mouse_x = event.pos[0] // scale_factor
            mouse_y = event.pos[1] // scale_factor
            
            # Add camera offset
            mouse_x += self.game.camera.viewport.x
            mouse_y += self.game.camera.viewport.y
            
            grid_x = mouse_x // GRID_SIZE
            grid_y = mouse_y // GRID_SIZE
            
            if (0 <= grid_x < len(self.game.state.grid[0])) and (0 <= grid_y < len(self.game.state.grid)):
                if self.game.state.grid[grid_y][grid_x] == 0:  # Walkable
                    self.game.state.target_pos = (grid_x, grid_y)
                    self.game.state.path = self.game.pathfinder.bfs(
                        self.game.state.player_grid_pos,
                        self.game.state.target_pos,
                        self.game.state.grid
                    )

    def handle_key_press(self, event):
        if event.key == KEYBINDS["quit"]:
            self.game.quit_game()
        elif event.key == KEYBINDS["reset"]:
            self.game.state.reset()