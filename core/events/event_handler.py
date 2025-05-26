#event_handler.py
import pygame
from core.events.input_handler import InputHandler

class EventHandler:
    def __init__(self, game):
        self.game = game
        self.input_handler = InputHandler(game)  # Pass the game reference

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.quit_game()
            elif event.type == pygame.VIDEORESIZE:
                # Handle window resizing if needed
                pass
            else:
                self.input_handler.handle_event(event)