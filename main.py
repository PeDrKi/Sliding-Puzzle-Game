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
        result = home.run(screen)
        
        if result is None or result[0] is None:
            break
        
        grid_size, music_on = result
        game = PuzzleGame(grid_size, music_on)
        return_to_home = game.run(screen)
        
        if not return_to_home:
            break
    
    pygame.quit()

if __name__ == "__main__":
    main()
# COPYRIGHT by Perfect Dragon King (PDK)
