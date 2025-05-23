from settings import GRID_ROWS, GRID_COLS, GRID_SIZE
from core.map.map_loader import load_tiled_map
from core.algorithms.pathfinder import Pathfinder

class GameState:
    def __init__(self, grid):
        self.grid = grid
        self.player_grid_pos = (4, 4)  # Should be set to walkable position
        self.player_pixel_pos = [
            self.player_grid_pos[0] * GRID_SIZE + GRID_SIZE // 2,
            self.player_grid_pos[1] * GRID_SIZE + GRID_SIZE // 2
        ]
        self.target_pos = None
        self.path = []
        self.is_moving = False
        self.current_target_pixel = None
        self.movement_speed = 180  # pixels per second

    def find_walkable_position(self):
        """Find the first walkable position in the grid"""
        for y in range(len(self.grid)):
            for x in range(len(self.grid[0])):
                if self.grid[y][x] == 0:
                    return (x, y)
        return (GRID_COLS // 2, GRID_ROWS // 2)  # Fallback

    def is_walkable(self, x, y):
        return 0 <= x < len(self.grid[0]) and 0 <= y < len(self.grid) and self.grid[y][x] == 0
        
    def reset(self):
        """Reset the game state while preserving the loaded map"""
        self.player_grid_pos = (GRID_COLS // 2, GRID_ROWS // 2)
        self.player_pixel_pos = [
            self.player_grid_pos[0] * GRID_SIZE + GRID_SIZE // 2,
            self.player_grid_pos[1] * GRID_SIZE + GRID_SIZE // 2
        ]
        self.target_pos = None
        self.path = []
        self.is_moving = False
        self.current_target_pixel = None
    
    @property
    def player_pos(self):
        """Returns current grid position (read-only)"""
        return (
            int(self.player_pixel_pos[0] // GRID_SIZE),
            int(self.player_pixel_pos[1] // GRID_SIZE)
        )
    
    def update_player_position(self, dt):
        """Update smooth movement towards next path node"""
        if not self.path and not self.is_moving:
            return
            
        if not self.is_moving and self.path:
            next_grid_pos = self.path[0]
            self.current_target_pixel = (
                next_grid_pos[0] * GRID_SIZE + GRID_SIZE // 2,
                next_grid_pos[1] * GRID_SIZE + GRID_SIZE // 2
            )
            self.is_moving = True
        
        if self.is_moving:
            dx = self.current_target_pixel[0] - self.player_pixel_pos[0]
            dy = self.current_target_pixel[1] - self.player_pixel_pos[1]
            distance = (dx**2 + dy**2)**0.5
            
            if distance < 2:  # Snap to target
                self.player_pixel_pos = list(self.current_target_pixel)
                self.player_grid_pos = (
                    int(self.player_pixel_pos[0] // GRID_SIZE),
                    int(self.player_pixel_pos[1] // GRID_SIZE)
                )
                self.path.pop(0)
                self.is_moving = False
                
                if not self.path and self.player_grid_pos == self.target_pos:
                    self.target_pos = None
            else:
                move_dist = min(distance, self.movement_speed * dt)
                self.player_pixel_pos[0] += (dx / distance) * move_dist
                self.player_pixel_pos[1] += (dy / distance) * move_dist