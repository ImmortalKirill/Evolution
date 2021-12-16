from objects import *
from model import find_grid, change_coords
import pygame
import random

def game_field(screen, field: Field, interface_game_window):
    """draws field on the screen in game-play window"""
    grid = find_grid(field, interface_game_window)
    draw_life_cells(screen, field, grid)
    draw_grid(screen, grid)


def draw_grid(screen, grid):
    """draws grid on screen
    look of grid: (coordinate of top left corner, number of colons and rows
                    (x, y) - coordinates of top left cell))"""
    for i in range(grid[2]+1):
        pygame.draw.line(screen, (255, 255, 255),
                         (grid[0] + i*grid[4], grid[1]),
                         (grid[0] + i*grid[4], grid[1]+grid[4]*grid[3]), 1
                         )
    for i in range(grid[3]+1):
        pygame.draw.line(screen, (255, 255, 255),
                         (grid[0], grid[1] + i*grid[4]),
                         (grid[0] + grid[4]*grid[2], grid[1] + i*grid[4]), 1
                         )
        
        
def draw_life_cells(screen, field, grid):
    """draws life cells of a field on grid"""
    for i in range(grid[2]):
        for j in range(grid[3]):
            cell = field.cells[grid[5][0]+i][grid[5][1] - j]
            pygame.draw.rect(screen, cell.color_bg, (grid[4]*i + grid[0], grid[1] + j*grid[4], grid[4], grid[4]), 0)

            if cell.live > 0:
                pygame.draw.ellipse(screen, cell.color,
                                 (grid[4]*i + grid[0], grid[1] + j*grid[4],
                                  grid[4], grid[4]), 0)

                pygame.draw.ellipse(screen, 'white',
                                    (grid[4] * i + grid[0], grid[1] + j * grid[4],
                                     grid[4], grid[4]), 5)

                
                
def draw_game(screen, field, interface, settings):
    """draws game screen on par screen with field"""
    game_field(screen, field, interface.game_window)
    settings.draw_pen_rect(screen)
    interface.draw(screen)
    settings.draw(screen)




def draw_menu(main_menu, screen):
    """draws menu"""
    main_menu.draw(screen)
    
if __name__ == "__main__":
    print("This module is not for direct call!")