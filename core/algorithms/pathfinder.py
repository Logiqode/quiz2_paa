#pathfinder.py
from collections import deque
import heapq
import math

class Pathfinder:
    @staticmethod
    def bfs(start, end, tile_properties_grid, current_form):
        """Breadth-First Search pathfinding considering form-specific walkability.
           If the target 'end' is unreachable, finds a path to the closest reachable tile to 'end'.

        Args:
            start (tuple): The starting grid coordinates (x, y).
            end (tuple): The target grid coordinates (x, y).
            tile_properties_grid (list[list[dict]]): Grid containing tile properties.
            current_form (str): The player's current form (e.g., 'human', 'bat').

        Returns:
            list: A list of coordinates representing the path (excluding start), 
                  or [] if no path found or start is invalid.
        """
        height = len(tile_properties_grid)
        if height == 0:
            return []
        width = len(tile_properties_grid[0])
        form_walkable_key = f"{current_form}_walkable"

        # --- Helper function for Manhattan distance ---
        def manhattan_distance(p1, p2):
            return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

        # --- Validate Start Position --- 
        if not (0 <= start[0] < width and 0 <= start[1] < height and 
                tile_properties_grid[start[1]][start[0]].get(form_walkable_key, False)):
            print(f"Pathfinder BFS: Start position {start} is not walkable for form {current_form}.")
            return []
            
        # --- Handle case where start is the end ---
        if start == end:
             # Check if end is walkable, if so, path is empty (already there)
             if tile_properties_grid[start[1]][start[0]].get(form_walkable_key, False):
                 return []
             else: # Start is the end, but end is not walkable - this case is ambiguous, return no path
                 print(f"Pathfinder BFS: Start {start} is the same as End, but it's not walkable for form {current_form}.")
                 return []

        # --- BFS Initialization ---
        queue = deque([(start, [start])]) # Store (node, path_to_node)
        visited = {start}
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # 4-way movement

        closest_path_to_target = []
        min_dist_to_target = float('inf')
        target_walkable = (0 <= end[0] < width and 0 <= end[1] < height and 
                           tile_properties_grid[end[1]][end[0]].get(form_walkable_key, False))

        # --- BFS Loop ---
        while queue:
            (x, y), path = queue.popleft()

            # --- Check if current node is the target ---
            if (x, y) == end:
                # Target reached directly
                print(f"Pathfinder BFS: Direct path found to {end} for form {current_form}.")
                return path[1:]  # Exclude start position

            # --- Update closest reachable node found so far ---
            # Only consider nodes if the original target *itself* is not walkable
            # Or, always track the closest node in case the direct path is very long?
            # Let's track regardless, it might be useful later, but only return it if target is unwalkable or unreachable.
            current_dist = manhattan_distance((x, y), end)
            if current_dist < min_dist_to_target:
                min_dist_to_target = current_dist
                closest_path_to_target = path

            # --- Explore Neighbors ---
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                # Check bounds, walkability for the form, and if not visited
                if (0 <= nx < width and 0 <= ny < height and
                        tile_properties_grid[ny][nx].get(form_walkable_key, False) and
                        (nx, ny) not in visited):
                    visited.add((nx, ny))
                    new_path = path + [(nx, ny)]
                    queue.append(((nx, ny), new_path))

        # --- BFS Finished: Target Not Reached Directly ---
        if not target_walkable:
             print(f"Pathfinder BFS: Target {end} is not walkable for form {current_form}.")
             # Fallback: Path to the closest visited node
             if closest_path_to_target:
                 closest_node = closest_path_to_target[-1]
                 print(f"Pathfinder BFS: Returning path to closest reachable node {closest_node}.")
                 return closest_path_to_target[1:] # Exclude start node
             else:
                 # Should not happen if start was valid
                 print(f"Pathfinder BFS: No reachable nodes found at all for form {current_form} from {start}.")
                 return []
        else:
            # Target was walkable, but no path was found (e.g., isolated area)
            print(f"Pathfinder BFS: Target {end} is walkable but no path found from {start} for form {current_form}.")
            # Optional: Could still return path to closest node in this case?
            # For now, stick to requirement: only fallback if target itself is unwalkable or unreachable.
            # Let's refine: if target is walkable but unreachable, still go to closest?
            # User request: "if there's no path to the tile clicked" - implies unreachable OR unwalkable target.
            if closest_path_to_target:
                 closest_node = closest_path_to_target[-1]
                 print(f"Pathfinder BFS: Returning path to closest reachable node {closest_node} as target was unreachable.")
                 return closest_path_to_target[1:]
            else:
                 print(f"Pathfinder BFS: No reachable nodes found at all for form {current_form} from {start}.")
                 return []

    @staticmethod
    def dfs(start, end, tile_properties_grid, current_form):
        """Depth-First Search pathfinding considering form-specific walkability.
           NOTE: DFS does not guarantee the shortest path and is generally not suitable
           for finding the 'closest' reachable tile in a meaningful way. 
           This implementation remains unchanged and will only find a direct path.
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
        # DFS doesn't handle the 'closest' logic, so we still check if the target is walkable.
        # If the target isn't walkable, DFS as implemented here will correctly fail.
        if not (0 <= end[0] < width and 0 <= end[1] < height and 
                tile_properties_grid[end[1]][end[0]].get(form_walkable_key, False)):
             print(f"Pathfinder DFS: End position {end} is not walkable for form {current_form}. No path possible.")
             return []

        stack = [(start, [start])]
        visited = {start}
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        while stack:
            (x, y), path = stack.pop()

            if (x, y) == end:
                return path[1:]

            # Explore neighbors in DFS order (can lead to non-optimal paths)
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

    @staticmethod
    def astar(start, end, tile_properties_grid, current_form):
        """A* Search pathfinding considering form-specific walkability.
           Uses Manhattan distance as heuristic for grid-based movement.
           If the target 'end' is unreachable, finds a path to the closest reachable tile to 'end'.

        Args:
            start (tuple): The starting grid coordinates (x, y).
            end (tuple): The target grid coordinates (x, y).
            tile_properties_grid (list[list[dict]]): Grid containing tile properties.
            current_form (str): The player's current form (e.g., 'human', 'bat').

        Returns:
            list: A list of coordinates representing the optimal path (excluding start), 
                  or [] if no path found or start is invalid.
        """
        height = len(tile_properties_grid)
        if height == 0:
            return []
        width = len(tile_properties_grid[0])
        form_walkable_key = f"{current_form}_walkable"

        # --- Helper function for Manhattan distance (heuristic) ---
        def heuristic(p1, p2):
            return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

        # --- Validate Start Position --- 
        if not (0 <= start[0] < width and 0 <= start[1] < height and 
                tile_properties_grid[start[1]][start[0]].get(form_walkable_key, False)):
            print(f"Pathfinder A*: Start position {start} is not walkable for form {current_form}.")
            return []
            
        # --- Handle case where start is the end ---
        if start == end:
             # Check if end is walkable, if so, path is empty (already there)
             if tile_properties_grid[start[1]][start[0]].get(form_walkable_key, False):
                 return []
             else: # Start is the end, but end is not walkable - this case is ambiguous, return no path
                 print(f"Pathfinder A*: Start {start} is the same as End, but it's not walkable for form {current_form}.")
                 return []

        # --- A* Initialization ---
        # Priority queue: (f_score, g_score, position, path)
        # f_score = g_score + heuristic (total estimated cost)
        # g_score = actual cost from start to current position
        open_set = []
        heapq.heappush(open_set, (heuristic(start, end), 0, start, [start]))
        
        # Keep track of visited nodes and their best g_scores
        visited = {}
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # 4-way movement

        # For fallback to closest reachable tile
        closest_path_to_target = []
        min_dist_to_target = float('inf')
        target_walkable = (0 <= end[0] < width and 0 <= end[1] < height and 
                           tile_properties_grid[end[1]][end[0]].get(form_walkable_key, False))

        # --- A* Main Loop ---
        while open_set:
            f_score, g_score, (x, y), path = heapq.heappop(open_set)

            # Skip if we've already found a better path to this node
            if (x, y) in visited and visited[(x, y)] <= g_score:
                continue
            
            visited[(x, y)] = g_score

            # --- Check if current node is the target ---
            if (x, y) == end:
                print(f"Pathfinder A*: Optimal path found to {end} for form {current_form}.")
                return path[1:]  # Exclude start position

            # --- Update closest reachable node found so far ---
            current_dist = heuristic((x, y), end)
            if current_dist < min_dist_to_target:
                min_dist_to_target = current_dist
                closest_path_to_target = path

            # --- Explore Neighbors ---
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                
                # Check bounds and walkability for the form
                if not (0 <= nx < width and 0 <= ny < height and
                        tile_properties_grid[ny][nx].get(form_walkable_key, False)):
                    continue
                
                # Calculate new g_score (cost from start to neighbor)
                new_g_score = g_score + 1  # Each step costs 1
                
                # Skip if we've already found a better path to this neighbor
                if (nx, ny) in visited and visited[(nx, ny)] <= new_g_score:
                    continue
                
                # Calculate f_score (total estimated cost)
                h_score = heuristic((nx, ny), end)
                new_f_score = new_g_score + h_score
                
                # Add neighbor to open set
                new_path = path + [(nx, ny)]
                heapq.heappush(open_set, (new_f_score, new_g_score, (nx, ny), new_path))

        # --- A* Finished: Target Not Reached Directly ---
        if not target_walkable:
            print(f"Pathfinder A*: Target {end} is not walkable for form {current_form}.")
            # Fallback: Path to the closest visited node
            if closest_path_to_target:
                closest_node = closest_path_to_target[-1]
                print(f"Pathfinder A*: Returning path to closest reachable node {closest_node}.")
                return closest_path_to_target[1:] # Exclude start node
            else:
                # Should not happen if start was valid
                print(f"Pathfinder A*: No reachable nodes found at all for form {current_form} from {start}.")
                return []
        else:
            # Target was walkable, but no path was found (e.g., isolated area)
            print(f"Pathfinder A*: Target {end} is walkable but no path found from {start} for form {current_form}.")
            # Fallback to closest reachable node
            if closest_path_to_target:
                closest_node = closest_path_to_target[-1]
                print(f"Pathfinder A*: Returning path to closest reachable node {closest_node} as target was unreachable.")
                return closest_path_to_target[1:]
            else:
                print(f"Pathfinder A*: No reachable nodes found at all for form {current_form} from {start}.")
                return []