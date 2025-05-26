#main.py
import pygame
from settings import WIDTH, HEIGHT, TITLE
from core.game import Game


def show_menu(screen):
    font_large = pygame.font.SysFont(None, 48)
    font_medium = pygame.font.SysFont(None, 36)
    font_small = pygame.font.SysFont(None, 24)
    clock = pygame.time.Clock()
    selected_algorithm = None

    while selected_algorithm is None:
        screen.fill((30, 30, 30))

        # Title
        title = font_large.render("Select Pathfinding Algorithm", True, (255, 255, 255))
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 4))

        # Algorithm options
        y_offset = HEIGHT // 2 - 60
        
        # DFS option
        dfs_text = font_medium.render("(D) - Depth-First Search (DFS)", True, (100, 200, 100))
        screen.blit(dfs_text, (WIDTH // 2 - dfs_text.get_width() // 2, y_offset))
        
        dfs_desc = font_small.render("Fast but may not find optimal path", True, (150, 150, 150))
        screen.blit(dfs_desc, (WIDTH // 2 - dfs_desc.get_width() // 2, y_offset + 25))

        # BFS option
        y_offset += 70
        bfs_text = font_medium.render("(B) - Breadth-First Search (BFS)", True, (100, 150, 200))
        screen.blit(bfs_text, (WIDTH // 2 - bfs_text.get_width() // 2, y_offset))
        
        bfs_desc = font_small.render("Guaranteed shortest path but slower", True, (150, 150, 150))
        screen.blit(bfs_desc, (WIDTH // 2 - bfs_desc.get_width() // 2, y_offset + 25))

        # A* option
        y_offset += 70
        astar_text = font_medium.render("(A) - A* Search Algorithm", True, (200, 150, 100))
        screen.blit(astar_text, (WIDTH // 2 - astar_text.get_width() // 2, y_offset))
        
        astar_desc = font_small.render("Optimal path with better performance", True, (150, 150, 150))
        screen.blit(astar_desc, (WIDTH // 2 - astar_desc.get_width() // 2, y_offset + 25))

        # Instructions
        y_offset += 80
        instruction = font_small.render("Press the corresponding letter to select", True, (200, 200, 200))
        screen.blit(instruction, (WIDTH // 2 - instruction.get_width() // 2, y_offset))

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
                elif event.key == pygame.K_a:
                    selected_algorithm = "ASTAR"
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

    return selected_algorithm


def show_algorithm_info(screen, algorithm):
    """Display information about the selected algorithm briefly"""
    font = pygame.font.SysFont(None, 36)
    clock = pygame.time.Clock()
    
    # Show for 2 seconds
    start_time = pygame.time.get_ticks()
    duration = 2000  # 2 seconds
    
    algorithm_info = {
        "DFS": {
            "name": "Depth-First Search",
            "description": "Explores as far as possible along each branch",
            "pros": "Fast execution, low memory usage",
            "cons": "May not find optimal path"
        },
        "BFS": {
            "name": "Breadth-First Search", 
            "description": "Explores all neighbors before going deeper",
            "pros": "Guaranteed shortest path",
            "cons": "Higher memory usage, slower"
        },
        "ASTAR": {
            "name": "A* Search Algorithm",
            "description": "Uses heuristic to guide search efficiently",
            "pros": "Optimal path with better performance",
            "cons": "Slightly more complex calculations"
        }
    }
    
    info = algorithm_info.get(algorithm, {})
    
    while pygame.time.get_ticks() - start_time < duration:
        screen.fill((40, 40, 60))
        
        # Title
        title = font.render(f"Selected: {info.get('name', algorithm)}", True, (255, 255, 255))
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 60))
        
        # Description
        desc = pygame.font.SysFont(None, 24).render(info.get('description', ''), True, (200, 200, 200))
        screen.blit(desc, (WIDTH // 2 - desc.get_width() // 2, HEIGHT // 2 - 20))
        
        # Loading text
        loading = pygame.font.SysFont(None, 24).render("Starting game...", True, (150, 150, 150))
        screen.blit(loading, (WIDTH // 2 - loading.get_width() // 2, HEIGHT // 2 + 20))
        
        pygame.display.flip()
        clock.tick(60)
        
        # Handle quit events during loading
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TITLE)

    # Show algorithm selection menu
    algorithm = show_menu(screen)
    
    # Show selected algorithm info
    show_algorithm_info(screen, algorithm)
    
    # Start the game with selected algorithm
    print(f"Starting game with {algorithm} algorithm...")
    game = Game(screen, algorithm=algorithm)  # Pass the selected algorithm
    game.run()

    pygame.quit()


if __name__ == "__main__":
    main()