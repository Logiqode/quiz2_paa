from settings import GRID_ROWS, GRID_COLS, GRID_SIZE
from core.map.map_loader import load_tiled_map
from core.algorithms.pathfinder import Pathfinder

class GameState:
    def __init__(self, tile_properties_grid):
        """Initializes the game state.

        Args:
            tile_properties_grid (list[list[dict]]): The grid containing tile properties,
                                                    including form-specific walkability.
        """
        self.tile_properties_grid = tile_properties_grid
        self.current_form = 'human'  # Default form
        self.forms = ['human', 'bat', 'rat']
        
        # Find initial spawn position based on the default form
        self.player_grid_pos = self.find_walkable_position(self.current_form)
        if not self.player_grid_pos:
            print("Warning: No walkable starting position found for default form! Placing at center.")
            self.player_grid_pos = (GRID_COLS // 2, GRID_ROWS // 2) # Fallback
            
        self.player_pixel_pos = [
            self.player_grid_pos[0] * GRID_SIZE + GRID_SIZE // 2,
            self.player_grid_pos[1] * GRID_SIZE + GRID_SIZE // 2
        ]
        self.target_pos = None
        self.path = []
        self.is_moving = False
        self.current_target_pixel = None
        self.movement_speed = 240  # pixels per second

    def find_walkable_position(self, form):
        """Find the first position walkable by the specified form."""
        form_walkable_key = f"{form}_walkable"
        height = len(self.tile_properties_grid)
        if height == 0:
            return None
        width = len(self.tile_properties_grid[0])
        
        for y in range(height):
            for x in range(width):
                if self.tile_properties_grid[y][x].get(form_walkable_key, False):
                    return (x, y)
        return None # No walkable position found for this form

    def is_walkable(self, x, y):
        """Checks if the grid cell (x, y) is walkable by the current form."""
        height = len(self.tile_properties_grid)
        if height == 0:
            return False
        width = len(self.tile_properties_grid[0])
        
        if 0 <= x < width and 0 <= y < height:
            form_walkable_key = f"{self.current_form}_walkable"
            return self.tile_properties_grid[y][x].get(form_walkable_key, False)
        return False
        
    def set_form(self, new_form):
        """Changes the player's current form.
        
        Args:
            new_form (str): The name of the form to switch to (e.g., 'human', 'bat', 'rat').
        """
        if new_form in self.forms:
            if self.current_form != new_form:
                print(f"Switching form to: {new_form}")
                self.current_form = new_form
                # Check if the current tile is still walkable for the new form
                current_x, current_y = self.player_pos
                if not self.is_walkable(current_x, current_y):
                    print(f"Warning: Current position ({current_x}, {current_y}) is not walkable for {new_form}!")
                    # Consider moving the player to the nearest walkable tile or handling this case
                self.cancel_movement() # Stop current path/movement
        else:
            print(f"Warning: Unknown form '{new_form}' requested.")
            
    def cancel_movement(self):
        """Stops current movement and clears the path."""
        self.path = []
        self.target_pos = None
        self.is_moving = False
        self.current_target_pixel = None
        print("Movement cancelled.")

    def reset(self):
        """Reset the game state."""
        self.current_form = 'human' # Reset to default form
        self.player_grid_pos = self.find_walkable_position(self.current_form)
        if not self.player_grid_pos:
             self.player_grid_pos = (GRID_COLS // 2, GRID_ROWS // 2)
        self.player_pixel_pos = [
            self.player_grid_pos[0] * GRID_SIZE + GRID_SIZE // 2,
            self.player_grid_pos[1] * GRID_SIZE + GRID_SIZE // 2
        ]
        self.cancel_movement()
    
    @property
    def player_pos(self):
        """Returns current grid position (read-only)"""
        return (
            int(self.player_pixel_pos[0] // GRID_SIZE),
            int(self.player_pixel_pos[1] // GRID_SIZE)
        )
    
    def update_player_position(self, dt):
        """Update smooth movement towards next path node"""
        if not self.is_moving and not self.path:
            # Not moving and no path, nothing to do
            return
            
        if not self.is_moving and self.path:
            # Start moving towards the next node in the path
            next_grid_pos = self.path[0]
            if not self.is_walkable(next_grid_pos[0], next_grid_pos[1]):
                print(f"Next path node {next_grid_pos} is not walkable for form {self.current_form}. Cancelling path.")
                self.cancel_movement()
                return
                
            self.current_target_pixel = (
                next_grid_pos[0] * GRID_SIZE + GRID_SIZE // 2,
                next_grid_pos[1] * GRID_SIZE + GRID_SIZE // 2
            )
            self.is_moving = True
        
        if self.is_moving:
            # If we are currently moving towards a target pixel
            if not self.current_target_pixel:
                 # Should not happen if is_moving is True, but safety check
                 print("Warning: is_moving is True but current_target_pixel is None. Cancelling movement.")
                 self.cancel_movement()
                 return
                 
            dx = self.current_target_pixel[0] - self.player_pixel_pos[0]
            dy = self.current_target_pixel[1] - self.player_pixel_pos[1]
            distance = (dx**2 + dy**2)**0.5
            
            if distance < 2:  # Reached the target pixel (close enough)
                self.player_pixel_pos = list(self.current_target_pixel)
                self.player_grid_pos = (
                    int(self.player_pixel_pos[0] // GRID_SIZE),
                    int(self.player_pixel_pos[1] // GRID_SIZE)
                )
                
                # --- FIX: Check if path is not empty before popping --- 
                if self.path:
                    self.path.pop(0) # Remove the node we just reached
                else:
                    # This case might indicate a logic issue if is_moving was true but path was empty
                    # For now, just log a warning.
                    print("Warning: Reached target pixel, but path was already empty.")
                # --- End of FIX --- 
                
                self.is_moving = False # Stop moving until the next node is processed (if any)
                self.current_target_pixel = None # Clear the pixel target
                
                if not self.path:
                    # Path is now complete
                    self.target_pos = None 
                    # print("Path complete.") # Optional debug message
                    
            else:
                # Move towards the target pixel
                move_dist = min(distance, self.movement_speed * dt)
                self.player_pixel_pos[0] += (dx / distance) * move_dist
                self.player_pixel_pos[1] += (dy / distance) * move_dist

