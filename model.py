import math
from objects import *


def step(Field):
    '''
    Field - class of Field
    
    Method generate new field by basics rules
    '''
    neighbors_live = 3
    neighbors_exist_start = 2
    neighbors_exist_end = 3
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
                if neighbors < neighbors_exist_start or neighbors > neighbors_exist_end:
                    pole[x][y].live -= 1
            else:
                if neighbors == neighbors_live:
                    pole[x][y].live += 1
    Field.cells = pole.copy()
    

def change_scale(field, par):
    """changes scale of field, increases it if par = 1, decreases it if par = -1"""
    change_step = 5
    field.scale += par * change_step
    if field.scale <= 5:
        field.scale = 5
            
def find_grid(field, game_window):  # FixMe Rail task, now returns grid for all field
    """calculates optimal grid size to display it in game_window
    look of grid: (coordinate of top left corner, number of rows and colons, size of 1 cell,
                    (x, y) - coordinates of top left cell)
    game_window - array of coordinates of left upper corner, lenth and height of window"""
    game_window_x_center = game_window[0] + game_window[2] / 2
    game_window_y_center = game_window[1] + game_window[3] / 2
    cell_size = field.scale
    grid = [0, 0, 0, 0, 0, 0]
    # calculating x coordinate of a grid
    dist_x = (game_window_x_center - game_window[0])/cell_size
    x = field.x_center - dist_x
    X = math.floor(x) - 2
    # calculating y coordinate of a grid in field coors
    dist_y = (game_window_y_center - game_window[1])/cell_size
    y = field.y_center + dist_y
    Y = math.ceil(y) + 2
    # cheking edges
    if X >= field.size_x:
        X = field.size_x - 1
    elif X < 0:
        X = 0
    if Y >= field.size_y:
        Y = field.size_y - 1
    elif Y < 0:
        Y = 0
    grid[0], grid[1] = change_coords((X, Y), cell_size, field.x_center, field.y_center, game_window, 1)
    grid[2] = math.ceil(game_window[2]/cell_size) + 5
    grid[3] = math.ceil(game_window[3]/cell_size) + 5
    if grid[2]+X >= field.size_x:
        grid[2] = field.size_x - X
    if Y - grid[3] < 0:
        grid[3] = Y
    grid[4] = cell_size
    grid[5] = (X, Y)

    return grid

def mouse_pos_check(mouse_pos, rect):
    """checks if mouse is on rect(left up angle, width, height)"""
    if abs(mouse_pos[0] - (rect[0]+rect[2] / 2)) <= rect[2] / 2 and abs(mouse_pos[1] - (rect[1]+rect[3] / 2)) <= rect[3] / 2:
        return True
    else:
        return False

def get_steps(loop_counter, speed):
    """calculates number of steps we should do in this loop
    par speed: if speed <= 0 return 0 else it's number from 1 to 10
    speed = x means that field_step will work each x game loop  """
    if speed <= 0:
        return 0
    else:
        if loop_counter%speed == 0:
            return 1
        else: return 0
    
    
def find_cell(pos, field, game_window):
    """finds coordinate of the cells which contains pos = (x,y) coordinate in pygame cors """

    x, y = change_coords(pos, field.scale, field.x_center, field.y_center, game_window, 0)
    if math.floor(x) >= field.size_x or math.floor(x) < 0 or math.ceil(y) >= field.size_y or math.ceil(y) <  0:
        return None, None
    else:
        return math.floor(x), math.ceil(y)
def change_coords(pos, cell_size, field_x_center, field_y_center, game_window, par_of_change):
    """changes coordinates from field coors to pygame coors
    par of change = 1 if Field coors in pygame, 0 if Pygame coors in field"""
    game_window_x_center = game_window[0] + game_window[2] / 2
    game_window_y_center = game_window[1] + game_window[3] / 2
    if par_of_change == 0:
        x_in_center = pos[0] - game_window_x_center
        y_in_center = pos[1] - game_window_y_center
        x_in_field = x_in_center/cell_size + field_x_center
        y_in_field = - y_in_center/cell_size + field_y_center
        return x_in_field, y_in_field
    elif par_of_change == 1:
        x, y = (pos[0]*cell_size, pos[1]*cell_size)
        X = game_window_x_center + x - field_x_center*cell_size
        Y = game_window_y_center - (y - field_y_center*cell_size)
        return X, Y

if __name__ == "__main__":
    print("This module is not for direct call!")

        
            