from core.game_state import GameState
from core.map.map_renderer import MapRenderer
import pygame
from settings import FPS, BLACK, WIDTH, HEIGHT
from core.map.tileset_manager import TilesetManager
from core.algorithms.pathfinder import Pathfinder
from core.map.map_loader import load_tiled_map
from core.events.event_handler import EventHandler
from settings import GRID_SIZE, GRID_COLS, GRID_ROWS
from core.camera import Camera

class Game:
    def __init__(self, screen, algorithm):
        self.screen = screen
        self.running = True
        self.clock = pygame.time.Clock()
        self.scale_factor = 2
        self.algorithm = algorithm  
        self.base_width = WIDTH // self.scale_factor
        self.base_height = HEIGHT // self.scale_factor
        
        # --- Initialize systems --- 
        
        # Load map data and the new tile properties grid
        # The first returned value is now tile_properties_grid
        self.tile_properties_grid, self.tiled_data = load_tiled_map("assets/maps/TiledMap1.2_PAA.json")
        
        # Initialize Pathfinder (it's static methods, so just need the class)
        self.pathfinder = Pathfinder()
        
        # Initialize GameState with the tile_properties_grid
        self.state = GameState(self.tile_properties_grid)
        
        # Initialize camera
        map_pixel_width = self.tiled_data["width"] * GRID_SIZE
        map_pixel_height = self.tiled_data["height"] * GRID_SIZE
        self.camera = Camera(self.base_width, self.base_height, map_pixel_width, map_pixel_height)
        
        # Initialize renderer
        self.tileset_manager = TilesetManager()
        for tileset in self.tiled_data.get("tilesets", []):
            # Ensure tileset loading uses the correct path if needed
            # Assuming load_tileset handles relative paths or uses a base asset path
            self.tileset_manager.load_tileset(tileset)
        
        # Create base surface for rendering
        self.base_surface = pygame.Surface((self.base_width, self.base_height))
        self.renderer = MapRenderer(self.base_surface, self.tileset_manager)
        
        # Initialize event handling
        self.event_handler = EventHandler(self)
    
    # Removed find_walkable_position as it's now handled in GameState
    
    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0 # Get delta time in seconds
            self.event_handler.process_events()
            self.update(dt)
            self.draw()
    
    def update(self, dt):
        # Pass delta time to player position update for smooth movement
        self.state.update_player_position(dt)
        
        # Update camera to follow player's pixel position
        self.camera.update(self.state.player_pixel_pos)
    
    def draw(self):
        # Clear base surface
        self.base_surface.fill(BLACK) # Use defined BLACK color
        
        # Draw everything to base surface (original scale)
        # Pass game_state, tiled_data, and camera to the renderer
        self.renderer.draw(self.state, self.tiled_data, self.camera)
        
        # Scale up to display surface
        scaled_surface = pygame.transform.scale(
            self.base_surface,
            (self.base_width * self.scale_factor,
            self.base_height * self.scale_factor)
        )
        self.screen.blit(scaled_surface, (0, 0))
        
        pygame.display.flip()
    
    def quit_game(self):
        print("Quitting game...")
        self.running = False

