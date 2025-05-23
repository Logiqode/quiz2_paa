import pygame
import os

class TilesetManager:
    def __init__(self, base_path="assets/tilesets/"):
        self.base_path = base_path
        self.tilesets = {}  # {firstgid: (image_surface, columns, tilecount)}
        self.tile_cache = {}  # {gid: subsurface}
    
    def load_tileset(self, tileset_data):
        """Load a tileset from Tiled data"""
        image_path = os.path.join(self.base_path, tileset_data["image"].replace("Tilesets/", ""))
        try:
            image = pygame.image.load(image_path).convert_alpha()
            self.tilesets[tileset_data["firstgid"]] = (
                image,
                tileset_data["columns"],
                tileset_data["tilecount"],
                tileset_data["tilewidth"],
                tileset_data["tileheight"]
            )
        except Exception as e:
            print(f"Failed to load tileset {image_path}: {e}")
    
    def get_tile(self, gid):
        """Get a subsurface for a specific tile GID"""
        if gid in self.tile_cache:
            return self.tile_cache[gid]
        
        # Find which tileset this GID belongs to
        for firstgid, (image, columns, tilecount, tw, th) in sorted(
            self.tilesets.items(), reverse=True):
            if gid >= firstgid:
                local_id = gid - firstgid
                if local_id < tilecount:
                    x = (local_id % columns) * tw
                    y = (local_id // columns) * th
                    tile = image.subsurface(pygame.Rect(x, y, tw, th))
                    self.tile_cache[gid] = tile
                    return tile
        
        return None  # Tile not found