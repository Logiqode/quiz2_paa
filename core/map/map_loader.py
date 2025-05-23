import json
from collections import defaultdict

def load_tiled_map(filename):
    """Loads a Tiled JSON map, extracts tile properties for different forms,
       and returns a grid representing these properties along with the raw map data.
       Handles default walkability based on a general layer 'walkable' property.

    Args:
        filename (str): Path to the Tiled JSON map file.

    Returns:
        tuple: A tuple containing:
            - tile_properties_grid (list[list[dict]]): A 2D list where each cell
              contains a dictionary of properties for the tile at that location,
              specifically focusing on 'human_walkable', 'bat_walkable',
              and 'rat_walkable'.
            - tiled_data (dict): The raw loaded JSON data from the Tiled map.
    """
    with open(filename) as f:
        data = json.load(f)

    width = data["width"]
    height = data["height"]

    # Initialize grid to store properties for each tile
    tile_properties_grid = [[defaultdict(bool) for _ in range(width)] for _ in range(height)]
    forms = ["human", "bat", "rat"]
    form_walkable_keys = [f"{form}_walkable" for form in forms]

    # --- 1. Collect tile-specific properties from tilesets --- 
    tile_prop_map = defaultdict(lambda: defaultdict(bool)) # Default properties to False
    for tileset in data.get("tilesets", []):
        firstgid = tileset.get("firstgid", 1)
        if "tiles" in tileset:
            for tile_def in tileset["tiles"]:
                tile_id = tile_def["id"]
                gid = tile_id + firstgid
                if "properties" in tile_def:
                    tile_props = {} # Store properties found for this specific tile GID
                    for prop in tile_def["properties"]:
                        prop_name = prop.get("name")
                        prop_type = prop.get("type")
                        prop_value = prop.get("value")
                        # Store general walkable and specific form walkables
                        if prop_name == "walkable" and prop_type == "bool":
                            tile_props["walkable"] = prop_value
                        elif prop_name in form_walkable_keys and prop_type == "bool":
                            tile_props[prop_name] = prop_value
                    if tile_props: # Only add if properties were found
                         tile_prop_map[gid].update(tile_props)

    # --- 2. Process layers to apply properties to the grid --- 
    for layer in data.get("layers", []):
        if layer.get("type") == "tilelayer" and layer.get("visible", True):
            layer_data = layer.get("data", [])
            layer_width = layer.get("width", width)
            layer_height = layer.get("height", height)

            # Get layer-wide properties (general and form-specific)
            layer_general_walkable = False
            layer_form_defaults = defaultdict(bool)
            if "properties" in layer:
                for prop in layer["properties"]:
                    prop_name = prop.get("name")
                    prop_type = prop.get("type")
                    prop_value = prop.get("value")
                    if prop_name == "walkable" and prop_type == "bool":
                        layer_general_walkable = prop_value
                    elif prop_name in form_walkable_keys and prop_type == "bool":
                        layer_form_defaults[prop_name] = prop_value

            # Apply properties to grid cells
            for y in range(layer_height):
                for x in range(layer_width):
                    if y >= height or x >= width: continue
                        
                    index = y * layer_width + x
                    if index < len(layer_data):
                        tile_gid = layer_data[index]
                        
                        if tile_gid > 0: # Only process actual tiles
                            # Get properties specific to this tile GID
                            tile_specific_props = tile_prop_map.get(tile_gid, {})
                            
                            # Determine final properties for this tile location (x, y)
                            final_props = {}
                            # Check if the tile itself has a general 'walkable' property defined
                            tile_general_walkable = tile_specific_props.get("walkable", layer_general_walkable)

                            for form_key in form_walkable_keys:
                                # Priority:
                                # 1. Tile-specific form property (e.g., tile's bat_walkable)
                                # 2. Layer-specific form property (e.g., layer's bat_walkable)
                                # 3. General walkability (tile's walkable > layer's walkable)
                                if form_key in tile_specific_props:
                                    final_props[form_key] = tile_specific_props[form_key]
                                elif form_key in layer_form_defaults:
                                    final_props[form_key] = layer_form_defaults[form_key]
                                else:
                                    # Default to the determined general walkability for this tile/layer
                                    final_props[form_key] = tile_general_walkable 
                            
                            # Update the grid cell, overwriting properties from lower layers
                            tile_properties_grid[y][x].update(final_props)

    return tile_properties_grid, data

