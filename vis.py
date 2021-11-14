from objects import *
from model import find_grid
import pygame
def menu_draw():
    pass # FixMe
    """ draws menu of the game with play button"""


def draw_interface():
    pass # FixMe
    """draws interface of the game with buttons and game-play window"""


def game_field(screen, field: Field, game_window):
    """draws field on the screen in game-play window"""
    grid = find_grid(field, game_window)
    draw_grid(screen, grid)

def draw_grid(screen, grid):
    """draws grid on screen
    look of grid: (coordinate of top left corner, number of colons and rows)"""
    for i in range(grid[2]+1):
        pygame.draw.line(screen, (255, 255, 255),
                         (grid[0] + i*grid[4], grid[1]),
                         (grid[0] + i*grid[4], grid[1]+grid[4]*grid[3]), 5
                         )
    for i in range(grid[3]+1):
        pygame.draw.line(screen, (255, 255, 255),
                         (grid[0], grid[1] + i*grid[4]),
                         (grid[0] + grid[4]*grid[2], grid[1] + i*grid[4]), 5
                         )
def draw_game(screen, field, game_window):
    """draws game screen on par screen with field"""
    game_field(screen, field, game_window)
    draw_interface()
    
    
if __name__ == "__main__":
    print("This module is not for direct call!")