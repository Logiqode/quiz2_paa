# from settings import GRID_SIZE

# class Player:
#     def __init__(self, grid_pos):
#         self.grid_pos = grid_pos
#         self.pixel_pos = [grid_pos[0] * GRID_SIZE, grid_pos[1] * GRID_SIZE]
#         self.speed = 200  # pixels per second
#         self.target_pos = None
#         self.moving = False

#     def update(self, dt):
#         if not self.moving:
#             return
            
#         dx = self.target_pos[0] - self.pixel_pos[0]
#         dy = self.target_pos[1] - self.pixel_pos[1]
#         distance = (dx**2 + dy**2)**0.5
        
#         if distance < 5:  # Snap to target
#             self.pixel_pos = self.target_pos
#             self.moving = False
#         else:
#             self.pixel_pos[0] += (dx / distance) * self.speed * dt
#             self.pixel_pos[1] += (dy / distance) * self.speed * dt

#     def move_to(self, grid_pos):
#         self.target_pos = [grid_pos[0] * GRID_SIZE, grid_pos[1] * GRID_SIZE]
#         self.moving = True