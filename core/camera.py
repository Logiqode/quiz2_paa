# camera.py
import pygame

class Camera:
    def __init__(self, screen_width, screen_height, map_pixel_width, map_pixel_height):
        self.viewport = pygame.Rect(0, 0, screen_width, screen_height)
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.map_width = map_pixel_width
        self.map_height = map_pixel_height
        self.smooth_speed = 0.2  # Adjust for smoother following (0.05-0.2 works well)
        
    def apply(self, pos):
        """Convert world coordinates to screen coordinates"""
        return (pos[0] - self.viewport.x, pos[1] - self.viewport.y)
    
    def update(self, target_pixel_pos):
        """Smoothly follow the target's pixel position"""
        # Calculate target camera position (centered on player)
        target_x = target_pixel_pos[0] - self.screen_width // 2
        target_y = target_pixel_pos[1] - self.screen_height // 2
        
        # Smooth camera movement
        self.viewport.x += (target_x - self.viewport.x) * self.smooth_speed
        self.viewport.y += (target_y - self.viewport.y) * self.smooth_speed
        
        # Clamp to map boundaries
        self.viewport.x = max(0, min(self.viewport.x, self.map_width - self.viewport.width))
        self.viewport.y = max(0, min(self.viewport.y, self.map_height - self.viewport.height))