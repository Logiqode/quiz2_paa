def get_reachable_area(start_x, start_y, tile_map):
    from collections import deque
    reachable = set()
    queue = deque([(start_x, start_y)])
    reachable.add((start_x, start_y))

    height, width = tile_map.shape
    while queue:
        x, y = queue.popleft()
        for nx, ny in [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]:
            if 0 <= nx < width and 0 <= ny < height:
                if (nx, ny) not in reachable:
                    if tile_map[ny, nx] == 0:  # Only walkable tiles (0)
                        reachable.add((nx, ny))
                        queue.append((nx, ny))
    return reachable

def can_move_to(x, y, tile_map, reachable_area):
    return (x, y) in reachable_area

def handle_mouse_click(event, player_pos, tile_map, tile_size, reachable_area_ref):
    mx, my = event.pos
    tx, ty = mx // tile_size, my // tile_size
    if can_move_to(tx, ty, tile_map, reachable_area_ref[0]):
        player_pos["x"], player_pos["y"] = tx, ty
        reachable_area_ref[0] = get_reachable_area(tx, ty, tile_map)
