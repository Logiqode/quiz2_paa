from collections import deque

class Pathfinder:
    @staticmethod
    def bfs(start, end, grid):
        """Breadth-First Search pathfinding"""
        if start == end:
            return []
        
        queue = deque([(start, [start])])
        visited = set([start])
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # 4-way movement
        
        while queue:
            (x, y), path = queue.popleft()
            
            if (x, y) == end:
                return path[1:]  # Exclude start position
            
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if (0 <= nx < len(grid[0]) and 0 <= ny < len(grid) and 
                    grid[ny][nx] == 0 and (nx, ny) not in visited):
                    visited.add((nx, ny))
                    queue.append(((nx, ny), path + [(nx, ny)]))
        
        return []  # No path found