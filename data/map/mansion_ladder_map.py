import numpy as np

# Shared ladder submap (2x3)
# 4 = ladder, 3 = container, 0 = walkable
MANSION_LADDER_SUBMAP = np.array([
    [4, 0, 4],  # Top row: ladders at [0][0] and [0][2]
    [3, 0, 0],  # Bottom row: a container under ladder A
], dtype=int)
