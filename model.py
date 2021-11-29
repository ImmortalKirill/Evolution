import math
from objects import *


def step(Field):
    '''
    Field - class of Field
    
    Method generate new field by basics rules
    '''
    def muavr_neighbors(field, neighbors, x, y):
        for i in range(x - 1, (x + 2) % field.size_x, 1):
            for j in range(y - 1, (y + 2) % field.size_y, 1):
                neighbors[i][j] += 1
                humidity[i][j] += field.cells[x][y].genes[0] / 8
        neighbors[x][y] -= 1 
        humidity[x][y] -= field.cells[x][y].genes[0] / 8
        
    def fraun_neighbors(field, neighbors, x, y):
        neighbors[x - 1][y] += 1
        humidity[x - 1][y] += field.cells[x][y].genes[0] / 4
        
        neighbors[x][(y + 1) % field.size_y] += 1
        humidity[x][(y + 1) % field.size_y] += field.cells[x][y].genes[0] / 4
        
        neighbors[x][y - 1] += 1
        humidity[x][y - 1] += field.cells[x][y].genes[0] / 4
        
        neighbors[(x + 1) % field.size_x][y] += 1  
        humidity[(x + 1) % field.size_x][y] += field.cells[x][y].genes[0] / 4
        
    def long_neighbors(field, neighbors, x, y):
        for i in range(x - 2, (x + 3) % field.size_x, 1):
            for j in range(y - 2, (y + 3) % field.size_y, 1):
                neighbors[i][j] += 1
                humidity[i][j] += field.cells[x][y].genes[0] / 24
        neighbors[x][y] -= 1
        humidity[x][y] -= field.cells[x][y].genes[0] / 24
        
    def born_survive(Field, neighbors, x, y):
        if Field.cells[x][y].live:
            if neighbors[x][y] < neighbors_exist_start or neighbors[x][y] > neighbors_exist_end:
                Field.cells[x][y].live -= 1
                #Field.cells[x][y].humidity = 0
        elif neighbors[x][y] == neighbors_born:
            Field.cells[x][y].live += 1
            Field.cells[x][y].genes[0] = humidity[x][y]
            
    neighbors_born = 3
    neighbors_exist_start = 2
    neighbors_exist_end = 3
    neighbors = [[0] * Field.size_y for i in range(Field.size_x)]
    humidity = [[0] * Field.size_y for i in range(Field.size_x)]
    for x in range(0, Field.size_x, 1): 
        for y in range(0, Field.size_y, 1):
            # counting number of neighbors
            if Field.cells[x][y].live:
                if Field.cells[x][y].genes[0] > Field.cells[x][y].humidity:
                    long_neighbors(Field, neighbors, x, y)
                else:
                    muavr_neighbors(Field, neighbors, x, y)
    for x in range(0, Field.size_x, 1): 
        for y in range(0, Field.size_y, 1):
            born_survive(Field, neighbors, x, y)
    
def mix_genes(cells_genes: list):
    """mixes genes of cells,
    cells_genes - list, consists of lists of tuples with cells genes"""
    humidity = 0
    radioactive = 0
    for i in cell_genes:
        humidity += i[0]
        radioactive += i[1]
    return humidity, radioactive

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
    par speed: if speed < 0 return 0 else it's fps of the game"""
    if speed <= 0:
        return 0
    elif speed == 10 or loop_counter % (11 - speed) == 0:
        return 1
    else:
        return 0
    
    
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

        
            