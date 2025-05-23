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
            
            # Use the GameState's is_walkable method which checks the current form
            if self.game.state.is_walkable(grid_x, grid_y):
                print(f"Target set to: ({grid_x}, {grid_y}) for form {self.game.state.current_form}")
                self.game.state.target_pos = (grid_x, grid_y)
                # Call pathfinder with tile_properties_grid and current_form
                if self.game.algorithm == "BFS":
                    self.game.state.path = self.game.pathfinder.bfs(
                        self.game.state.player_grid_pos,
                        self.game.state.target_pos,
                        self.game.state.tile_properties_grid,
                        self.game.state.current_form
                    )
                elif self.game.algorithm == "DFS":
                    self.game.state.path = self.game.pathfinder.dfs(
                        self.game.state.player_grid_pos,
                        self.game.state.target_pos,
                        self.game.state.tile_properties_grid,
                        self.game.state.current_form
                    )
                if not self.game.state.path and self.game.state.player_pos != self.game.state.target_pos:
                    print(f"No path found to ({grid_x}, {grid_y}) for form {self.game.state.current_form}")
                elif self.game.state.path:
                    print(f"Path found: {self.game.state.path}")
                    self.game.state.is_moving = False # Reset moving flag to start new path
            else:
                print(f"Clicked non-walkable tile ({grid_x}, {grid_y}) for form {self.game.state.current_form}")

    def handle_key_press(self, event):
        if event.key == KEYBINDS["quit"]:
            self.game.quit_game()
        elif event.key == KEYBINDS["reset"]:
            self.game.state.reset()
        # Form switching keys
        elif event.key == KEYBINDS["human"]:
            self.game.state.set_form("human")
        elif event.key == KEYBINDS["bat"]:
            self.game.state.set_form("bat")
        elif event.key == KEYBINDS["rat"]:
            self.game.state.set_form("rat")
        # Add other keybinds as needed

