import pygame
import Engine
import sys

engine = Engine

def Main():
    # Set the background color (RGB tuple)
    backgroundcolour = (180, 30, 255)

    # Create a Pygame window with the specified resolution
    screen = pygame.display.set_mode((1600, 1000))

    # Set the window title
    pygame.display.set_caption('Maze game')

    # Increase the recursion limit to handle larger mazes
    sys.setrecursionlimit(3000)
    # Call the game function from the imported engine module
    engine.game(screen, backgroundcolour)

    pygame.quit()

if __name__ == '__main__':
    Main()
