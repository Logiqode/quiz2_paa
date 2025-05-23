import json
from collections import defaultdict

def load_tiled_map(filename):
    with open(filename) as f:
        data = json.load(f)
    
    # Initialize empty grid (0=walkable, 1=obstacle)
    grid = [[0 for _ in range(data["width"])] for _ in range(data["height"])]
    tile_properties = defaultdict(dict)
    
    # Collect all tile properties from tilesets
    for tileset in data.get("tilesets", []):
        if "tiles" in tileset:
            for tile in tileset["tiles"]:
                if "properties" in tile:
                    for prop in tile["properties"]:
                        if prop["name"] == "walkable":
                            tile_properties[tile["id"] + tileset["firstgid"]] = prop["value"]
    
    # Process each layer
    for layer in data["layers"]:
        if layer["type"] == "tilelayer":
            layer_walkable = True  # Default to walkable unless layer has property
            if "properties" in layer:
                for prop in layer["properties"]:
                    if prop["name"] == "walkable":
                        layer_walkable = prop["value"]
            
            for y in range(layer["height"]):
                for x in range(layer["width"]):
                    tile_gid = layer["data"][y * layer["width"] + x]
                    if tile_gid > 0:  # Valid tile
                        # Check both tile-specific and layer-wide walkable property
                        is_walkable = tile_properties.get(tile_gid, layer_walkable)
                        if not is_walkable:
                            grid[y][x] = 1  # Mark as obstacle
    
    return grid, data