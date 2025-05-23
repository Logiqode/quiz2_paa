import pygame
from settings import WIDTH, HEIGHT, TITLE
from core.game import Game

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TITLE)
    
    game = Game(screen)  # Now passing the screen parameter
    game.run()
    
    pygame.quit()

if __name__ == "__main__":
    main()