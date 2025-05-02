import pygame
from constants import WINDOW_SIZE
from puzzle_game import PuzzleGame
from home import HomeScreen

def main():
    pygame.init()
    
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Puzzle Game")
    
    while True:
        home = HomeScreen()
        grid_size = home.run(screen)
        
        if grid_size is None:
            break
        
        game = PuzzleGame(grid_size)
        return_to_home = game.run(screen)
        
        if not return_to_home:
            break
    
    pygame.quit()

if __name__ == "__main__":
    main()
# COPYRIGHT by Perfect Dragon King (PDK)