import numpy as np

# Tile meanings
# 0 = walkable
# 1 = wall (unwalkable)
# 2 = obstacle (unwalkable, can change via interaction)
# 3 = container (interactable with spacebar)
# 4 = ladder (interactable)

TILE_MAP = np.array([
    [0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0, 0, 3, 1, 0, 0],
    [0, 0, 1, 0, 0, 0, 3, 1, 0, 0],
    [0, 4, 1, 0, 0, 0, 0, 0, 2, 0],
    [1, 1, 1, 1, 1, 0, 0, 1, 0, 1],
    [0, 4, 0, 0, 1, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 1, 0, 0],
    [0, 0, 0, 3, 1, 0, 0, 1, 0, 0],
], dtype=int)

