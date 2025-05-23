from core.game_state import GameState
from core.map.map_renderer import MapRenderer
import pygame
from settings import FPS, BLACK, WIDTH, HEIGHT
from core.map.tileset_manager import TilesetManager
from core.algorithms.pathfinder import Pathfinder
from core.map.map_loader import load_tiled_map
from core.events.event_handler import EventHandler
from settings import GRID_SIZE, GRID_COLS, GRID_ROWS

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        self.event_handler = EventHandler(self)
        
        # Load map and initialize pathfinder
        self.grid, self.tiled_data = load_tiled_map("assets/maps/TiledMap1_PAA.json")
        self.pathfinder = Pathfinder()
        
        # Initialize game state with the grid
        self.state = GameState(self.grid)
        self.state.player_grid_pos = self.find_walkable_position()  # Implement this
        
        # Initialize renderer
        self.tileset_manager = TilesetManager()
        for tileset in self.tiled_data["tilesets"]:
            self.tileset_manager.load_tileset(tileset)
        self.renderer = MapRenderer(screen, self.tileset_manager)
    
    def find_walkable_position(self):
        """Find first walkable position for player spawn"""
        for y in range(len(self.grid)):
            for x in range(len(self.grid[0])):
                if self.grid[y][x] == 0:
                    return (x, y)
        return (GRID_COLS//2, GRID_ROWS//2)  # Fallback
    
    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.event_handler.process_events()
            self.update()
            self.draw()
    
    def update(self):
        dt = self.clock.get_time() / 1000
        self.state.update_player_position(dt)
    
    def draw(self):
        self.screen.fill(BLACK)
        self.renderer.draw(self.state, self.tiled_data)
        # Draw other entities (player, etc.) here
        pygame.display.flip()
    
    def quit_game(self):
        self.running = False