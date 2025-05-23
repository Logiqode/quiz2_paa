import pygame
from settings import GRID_SIZE

class MapRenderer:
    def __init__(self, screen, tileset_manager):
        self.screen = screen
        self.tileset_manager = tileset_manager
    
    def draw(self, game_state, tiled_data):
        self.screen.fill((0, 0, 0))  # Clear screen
        
        # Draw tile layers
        for layer in tiled_data["layers"]:
            if layer["type"] == "tilelayer" and layer.get("visible", True):
                self.draw_tile_layer(layer, tiled_data["tilewidth"], tiled_data["tileheight"])
        
        # Draw path (blue circles)
        self.draw_path(game_state)
        
        # Draw player (green circle)
        self.draw_player(game_state)
        
        pygame.display.flip()
    
    def draw_path(self, game_state):
        """Draw the path as blue circles"""
        for x, y in game_state.path:
            center = (
                x * GRID_SIZE + GRID_SIZE // 2,
                y * GRID_SIZE + GRID_SIZE // 2
            )
            pygame.draw.circle(self.screen, (0, 0, 255), center, GRID_SIZE // 3)
    
    def draw_player(self, game_state):
        """Draw the player as a green circle"""
        pygame.draw.circle(
            self.screen, 
            (0, 255, 0),
            (int(game_state.player_pixel_pos[0]), int(game_state.player_pixel_pos[1])),
            GRID_SIZE // 2
        )

    def draw_tile_layer(self, layer, tile_width, tile_height):
        for y in range(layer["height"]):
            for x in range(layer["width"]):
                tile_gid = layer["data"][y * layer["width"] + x]
                if tile_gid > 0:
                    tile = self.tileset_manager.get_tile(tile_gid)
                    if tile:
                        self.screen.blit(tile, (x * tile_width, y * tile_height))
    
    def draw_collision_debug(self, game_state, tile_width, tile_height):
        for y in range(len(game_state.grid)):
            for x in range(len(game_state.grid[0])):
                if game_state.grid[y][x] == 1:  # Obstacle
                    rect = pygame.Rect(
                        x * tile_width, 
                        y * tile_height,
                        tile_width, 
                        tile_height
                    )
                    s = pygame.Surface((tile_width, tile_height), pygame.SRCALPHA)
                    s.fill((255, 0, 0, 32))
                    self.screen.blit(s, rect)