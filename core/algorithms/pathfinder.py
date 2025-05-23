from collections import deque

class Pathfinder:
    @staticmethod
    def bfs(start, end, tile_properties_grid, current_form):
        """Breadth-First Search pathfinding considering form-specific walkability.

        Args:
            start (tuple): The starting grid coordinates (x, y).
            end (tuple): The ending grid coordinates (x, y).
            tile_properties_grid (list[list[dict]]): Grid containing tile properties.
            current_form (str): The player's current form (e.g., 'human', 'bat').

        Returns:
            list: A list of coordinates representing the path (excluding start), or [] if no path found.
        """
        if start == end:
            return []

        height = len(tile_properties_grid)
        if height == 0:
            return []
        width = len(tile_properties_grid[0])
        form_walkable_key = f"{current_form}_walkable"

        # Check if start or end points are themselves unwalkable for the current form
        if not (0 <= start[0] < width and 0 <= start[1] < height and 
                tile_properties_grid[start[1]][start[0]].get(form_walkable_key, False)):
            print(f"Pathfinder BFS: Start position {start} is not walkable for form {current_form}.")
            return []
        if not (0 <= end[0] < width and 0 <= end[1] < height and 
                tile_properties_grid[end[1]][end[0]].get(form_walkable_key, False)):
            print(f"Pathfinder BFS: End position {end} is not walkable for form {current_form}.")
            return []

        queue = deque([(start, [start])])
        visited = {start}
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # 4-way movement

        while queue:
            (x, y), path = queue.popleft()

            if (x, y) == end:
                return path[1:]  # Exclude start position

            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                # Check bounds and form-specific walkability
                if (0 <= nx < width and 0 <= ny < height and
                        tile_properties_grid[ny][nx].get(form_walkable_key, False) and
                        (nx, ny) not in visited):
                    visited.add((nx, ny))
                    queue.append(((nx, ny), path + [(nx, ny)]))

        print(f"Pathfinder BFS: No path found from {start} to {end} for form {current_form}.")
        return []  # No path found

    @staticmethod
    def dfs(start, end, tile_properties_grid, current_form):
        """Depth-First Search pathfinding considering form-specific walkability.

        Args:
            start (tuple): The starting grid coordinates (x, y).
            end (tuple): The ending grid coordinates (x, y).
            tile_properties_grid (list[list[dict]]): Grid containing tile properties.
            current_form (str): The player's current form (e.g., 'human', 'bat').

        Returns:
            list: A list of coordinates representing the path (excluding start), or [] if no path found.
        """
        if start == end:
            return []

        height = len(tile_properties_grid)
        if height == 0:
            return []
        width = len(tile_properties_grid[0])
        form_walkable_key = f"{current_form}_walkable"

        # Check if start or end points are themselves unwalkable for the current form
        if not (0 <= start[0] < width and 0 <= start[1] < height and 
                tile_properties_grid[start[1]][start[0]].get(form_walkable_key, False)):
             print(f"Pathfinder DFS: Start position {start} is not walkable for form {current_form}.")
             return []
        if not (0 <= end[0] < width and 0 <= end[1] < height and 
                tile_properties_grid[end[1]][end[0]].get(form_walkable_key, False)):
             print(f"Pathfinder DFS: End position {end} is not walkable for form {current_form}.")
             return []

        stack = [(start, [start])]
        visited = {start}
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        while stack:
            (x, y), path = stack.pop()

            if (x, y) == end:
                return path[1:]

            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                # Check bounds and form-specific walkability
                if (0 <= nx < width and 0 <= ny < height and
                        tile_properties_grid[ny][nx].get(form_walkable_key, False) and
                        (nx, ny) not in visited):
                    visited.add((nx, ny))
                    stack.append(((nx, ny), path + [(nx, ny)]))

        print(f"Pathfinder DFS: No path found from {start} to {end} for form {current_form}.")
        return []  # No path found

