import pygame
from settings import GRID_SIZE, FORM_COLORS


DEFAULT_COLOR = (255, 255, 255)

class MapRenderer:
    def __init__(self, screen, tileset_manager):
        self.screen = screen
        self.tileset_manager = tileset_manager
    
    def draw(self, game_state, tiled_data, camera):
        
        for layer in tiled_data.get("layers", []):
            if layer.get("type") == "tilelayer" and layer.get("visible", True):
                tile_width = tiled_data.get("tilewidth", GRID_SIZE)
                tile_height = tiled_data.get("tileheight", GRID_SIZE)
                self.draw_tile_layer(layer, tile_width, tile_height, camera)
        
        self.draw_path(game_state, camera)
        
        self.draw_player(game_state, camera)
        

    def draw_path(self, game_state, camera):
        """Draw the path with camera-relative positions"""
        if game_state.path:
            for x, y in game_state.path:
                world_x = x * GRID_SIZE + GRID_SIZE // 2
                world_y = y * GRID_SIZE + GRID_SIZE // 2
                screen_x, screen_y = camera.apply((world_x, world_y))
                path_circle_surf = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
                pygame.draw.circle(path_circle_surf, (0, 0, 255, 100), (GRID_SIZE // 2, GRID_SIZE // 2), GRID_SIZE // 3)
                self.screen.blit(path_circle_surf, (screen_x - GRID_SIZE // 2, screen_y - GRID_SIZE // 2))
    
    def draw_player(self, game_state, camera):
        """Draw the player with camera-relative position, using sprite if available."""
        screen_x_center, screen_y_center = camera.apply(game_state.player_pixel_pos)

        player_sprite = game_state.get_current_player_sprite()

        if player_sprite:
            sprite_rect = player_sprite.get_rect(center=(int(screen_x_center), int(screen_y_center)))
            self.screen.blit(player_sprite, sprite_rect.topleft)
        else:
            player_color = FORM_COLORS.get(game_state.current_form, DEFAULT_COLOR)
            pygame.draw.circle(
                self.screen,
                player_color,
                (int(screen_x_center), int(screen_y_center)),
                GRID_SIZE // 2
            )

    def draw_tile_layer(self, layer, tile_width, tile_height, camera):
        layer_width = layer.get("width")
        layer_height = layer.get("height")
        layer_data = layer.get("data")
        
        if not layer_width or not layer_height or not layer_data:
            return
            
        start_col = max(0, int(camera.viewport.left // tile_width))
        end_col = min(layer_width, int(camera.viewport.right // tile_width) + 1)
        start_row = max(0, int(camera.viewport.top // tile_height))
        end_row = min(layer_height, int(camera.viewport.bottom // tile_height) + 1)

        for y in range(start_row, end_row):
            for x in range(start_col, end_col):
                index = y * layer_width + x
                if 0 <= index < len(layer_data):
                    tile_gid = layer_data[index]
                    if tile_gid > 0:
                        tile_surface = self.tileset_manager.get_tile(tile_gid)
                        if tile_surface:
                            world_x = x * tile_width
                            world_y = y * tile_height
                            screen_x, screen_y = camera.apply((world_x, world_y))
                            self.screen.blit(tile_surface, (int(screen_x), int(screen_y)))
    
    def draw_collision_debug(self, game_state, camera):
        """Draw collision debug based on form-specific walkability."""
        debug_surface = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        height = len(game_state.tile_properties_grid)
        if height == 0: return
        width = len(game_state.tile_properties_grid[0])
        form_walkable_key = f"{game_state.current_form}_walkable"

        for y in range(height):
            for x in range(width):
                if not game_state.tile_properties_grid[y][x].get(form_walkable_key, False):
                    world_x = x * GRID_SIZE
                    world_y = y * GRID_SIZE
                    screen_x, screen_y = camera.apply((world_x, world_y))
                    pygame.draw.rect(
                        debug_surface, 
                        (255, 0, 0, 64),
                        (int(screen_x), int(screen_y), GRID_SIZE, GRID_SIZE)
                    )
        
        self.screen.blit(debug_surface, (0, 0))

