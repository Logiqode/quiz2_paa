import pygame
from settings import WIDTH, HEIGHT, TITLE
from core.game import Game


def show_menu(screen):
    font = pygame.font.SysFont(None, 48)
    clock = pygame.time.Clock()
    selected_algorithm = None

    while selected_algorithm is None:
        screen.fill((30, 30, 30))

        title = font.render(
            "Select Algorithm: DFS (D) or BFS (B)", True, (255, 255, 255)
        )
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 3))

        pygame.display.flip()
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    selected_algorithm = "DFS"
                elif event.key == pygame.K_b:
                    selected_algorithm = "BFS"

    return selected_algorithm


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TITLE)

    algorithm = show_menu(screen)
    game = Game(screen, algorithm=algorithm)  # Pass the selected algorithm
    game.run()

    pygame.quit()


if __name__ == "__main__":
    main()
