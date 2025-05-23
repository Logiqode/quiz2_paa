import pygame
from settings import GRID_SIZE

class MapRenderer:
    def __init__(self, screen, tileset_manager):
        self.screen = screen
        self.tileset_manager = tileset_manager
    
    def draw(self, game_state, tiled_data, camera):
        self.screen.fill((0, 0, 0))
        
        # Draw tile layers with camera
        for layer in tiled_data["layers"]:
            if layer["type"] == "tilelayer" and layer.get("visible", True):
                self.draw_tile_layer(layer, tiled_data["tilewidth"], tiled_data["tileheight"], camera)
        
        # Draw path with camera
        self.draw_path(game_state, camera)
        
        # Draw player with camera
        self.draw_player(game_state, camera)
        
        pygame.display.flip()
    
    def draw_path(self, game_state, camera):
        """Draw the path with camera-relative positions"""
        path_surface = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        
        for x, y in game_state.path:
            world_x = x * GRID_SIZE + GRID_SIZE // 2
            world_y = y * GRID_SIZE + GRID_SIZE // 2
            screen_x, screen_y = camera.apply((world_x, world_y))
            pygame.draw.circle(path_surface, (0, 0, 255, 64), (screen_x, screen_y), GRID_SIZE // 3)
        
        self.screen.blit(path_surface, (0, 0))
    
    def draw_player(self, game_state, camera):
        """Draw the player with camera-relative position"""
        screen_x, screen_y = camera.apply(game_state.player_pixel_pos)
        pygame.draw.circle(
            self.screen, 
            (0, 255, 0),
            (int(screen_x), int(screen_y)),
            GRID_SIZE // 2
        )

    def draw_tile_layer(self, layer, tile_width, tile_height, camera):
        for y in range(layer["height"]):
            for x in range(layer["width"]):
                tile_gid = layer["data"][y * layer["width"] + x]
                if tile_gid > 0:
                    tile = self.tileset_manager.get_tile(tile_gid)
                    if tile:
                        world_x = x * tile_width
                        world_y = y * tile_height
                        # Only draw tiles visible in camera
                        if (camera.viewport.x - tile_width < world_x < camera.viewport.x + camera.viewport.width and
                            camera.viewport.y - tile_height < world_y < camera.viewport.y + camera.viewport.height):
                            screen_x, screen_y = camera.apply((world_x, world_y))
                            self.screen.blit(tile, (screen_x, screen_y))
    
    def draw_collision_debug(self, game_state, camera):
        """Draw collision debug with camera"""
        debug_surface = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        
        for y in range(len(game_state.grid)):
            for x in range(len(game_state.grid[0])):
                if game_state.grid[y][x] == 1:
                    world_x = x * GRID_SIZE
                    world_y = y * GRID_SIZE
                    screen_x, screen_y = camera.apply((world_x, world_y))
                    pygame.draw.rect(
                        debug_surface, 
                        (255, 0, 0, 32),
                        (screen_x, screen_y, GRID_SIZE, GRID_SIZE)
                    )
        
        self.screen.blit(debug_surface, (0, 0))