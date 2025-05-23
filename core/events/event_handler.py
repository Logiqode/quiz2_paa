import pygame
from core.events.input_handler import InputHandler

class EventHandler:
    def __init__(self, game):
        self.game = game
        self.input_handler = InputHandler(game)

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.quit_game()
            else:
                self.input_handler.handle_event(event)