import math
from objects import *


def step(Field):
    '''
    Field - class of Field
    
    Method generate new field by basics rules
    '''

    pole = [[0] * Field.size_y for i in range(Field.size_x)]
    for x in range(Field.size_x):
        for y in range(Field.size_y):
            object1 = Cell()
            object1.new_cell(x, y)
            object1.live = Field.cells[x][y].live
            pole[x][y] = object1
    for x in range(0, Field.size_x, 1): 
        for y in range(0, Field.size_y, 1):
            # counting number of neighbors
            neighbors = 0
            for i in range(-1, 2, 1):
                for j in range(-1, 2, 1):
                    if Field.cells[(x + i) % Field.size_x][(y + j) % Field.size_y].live:
                        neighbors += 1
            if Field.cells[x][y].live:
                neighbors -= 1
            # checking future for cell
            if Field.cells[x][y].live:
                if neighbors < 2 or neighbors > 3:
                    pole[x][y].live -= 1
            else:
                if neighbors == 3:
                    pole[x][y].live += 1
    Field.cells = pole.copy()
    

def change_scale(field, par):
    """changes scale of field, increases it if par = 1, decreases it if par = -1"""
    change_step = 10
    field.scale += par * change_step
    if field.scale <= 10:
        field.scale = 10
            
def find_grid(field, game_window):  # FixMe Rail task, now returns grid for all field
    """calculates optimal grid size to display it in game_window
    look of grid: (coordinate of top left corner, number of rows and colons, size of 1 cell,
                    (x, y) - coordinates of top left cell)
    game_window - array of coordinates of left upper corner, lenth and height of window"""
    game_window_x_center = game_window[0] + game_window[2] / 2
    game_window_y_center = game_window[1] + game_window[3] / 2
    cell_size = field.scale
    grid = [0, 0, 0, 0, 0, 0]
    grid[0] = game_window_x_center - field.x_center * field.scale
    grid[1] = game_window_y_center + field.scale * (-field.size_y + math.ceil(field.y_center) -
                                                   1 + (field.y_center - math.floor(field.y_center))
                                                   )
    if math.ceil(game_window[2]) > field.size_x:
        grid[2] = field.size_x
    else:
        grid[2] = math.ceil(game_window[2]) // field.scale
    grid[3] = field.size_y
    if math.ceil(game_window[3]) > field.size_y:
        grid[3] = field.size_y
    else:
        grid[3] = math.ceil(game_window[3]) // field.scale
    grid[4] = field.scale
    #grid[5] = (0, field.size_y)
    a = math.ceil(field.x_center) // field.scale - grid[2] // 2
    b = math.ceil(field.y_center) // field.scale - grid[3] // 2
    if a > field.size_x or a < 0:
        a = 0
    if b > field.size_y or b <= 0:
        b = field.size_y
    grid[5] = (a, b)
    return grid

def mouse_pos_check(mouse_pos, rect):
    """checks if mouse is on rect(left up angle, width, height)"""
    if abs(mouse_pos[0] - (rect[0]+rect[2] / 2)) <= rect[2] / 2 and abs(mouse_pos[1] - (rect[1]+rect[3] / 2)) <= rect[3] / 2:
        return True
    else:
        return False

def get_steps(loop_counter, speed):
    """calculates number of steps we should do in this loop"""
    return 1
if __name__ == "__main__":
    print("This module is not for direct call!")

        
            