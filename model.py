import math
import pygame
from random import randint
from numpy import array, zeros, floor, ceil
import concurrent.futures
from numba import njit, prange
import time
from itertools import repeat
# not in use for now

@njit(fastmath=True, cache=True)

def gen_out_of_range(gen):
    """checks if gen is in -100 to 100 range, else changes it"""
    if gen > 100:
        gen = 100
    elif gen < -100:
        gen = -100
    return gen
@njit(fastmath=True, cache=True)
def muavr_neighbors(cell_genes: list, neighbors1: list, genes_to_pass1: list, x, y, field_size_x, field_size_y):
        '''Count neighbors in area of nearest 8 cells'''
        for i in range(x - 1, (x + 2) % field_size_x, 1):
            for j in range(y - 1, (y + 2) % field_size_y, 1):
                neighbors1[i][j] += 1
                # adding parent gene
                genes_to_pass1[i][j][0] += cell_genes[0]
        neighbors1[x][y] -= 1
        genes_to_pass1[x][y][0] -= cell_genes[0]
        return neighbors1, genes_to_pass1

@njit(fastmath=True, cache=True)
def fraun_neighbors(cell_genes: list, neighbors1: list, genes_to_pass1: list, x, y, field_size_x, field_size_y):
        '''Count neighbors in 4 bordered cells'''
        neighbors1[x - 1][y] += 1
        genes_to_pass1[x - 1][y][0] += cell_genes[0]

        neighbors1[x][(y + 1) % field_size_y] += 1
        genes_to_pass1[x][(y + 1) % field_size_y][0] += cell_genes[0]

        neighbors1[x][y - 1] += 1
        genes_to_pass1[x][y - 1][0] += cell_genes[0]

        neighbors1[(x + 1) % field_size_x][y] += 1
        genes_to_pass1[(x + 1) % field_size_x][y][0] += cell_genes[0]
        return neighbors1, genes_to_pass1

@njit(fastmath=True, cache=True)
def long_neighbors(cell_genes: list, neighbors1: list, genes_to_pass1: list, x, y, field_size_x, field_size_y):
        '''Count neighbors in area of nearest 8 cells and more 4 cells on the distance 2cells away'''
        # closest 8 cells
        for i in range(x - 1, (x + 2) % field_size_x, 1):
            for j in range(y - 1, (y + 2) % field_size_y, 1):
                neighbors1[i][j] += 1
                # adding parent gene
                genes_to_pass1[i][j][0] += cell_genes[0]
        # additional 4 cells
        neighbors1[x - 2][y] += 1
        genes_to_pass1[x - 2][y][0] += cell_genes[0]

        neighbors1[x][(y + 2) % field_size_y] += 1
        genes_to_pass1[x][(y + 2) % field_size_y][0] += cell_genes[0]

        neighbors1[x][y - 2] += 1
        genes_to_pass1[x][y - 2][0] += cell_genes[0]

        neighbors1[(x + 2) % field_size_x][y] += 1
        genes_to_pass1[(x + 2) % field_size_x][y][0] += cell_genes[0]

        neighbors1[x][y] -= 1
        genes_to_pass1[x][y][0] -= cell_genes[0]
        return neighbors1, genes_to_pass1

@njit(fastmath=True, cache=True)
def divide_manager(cell_genes: list, neighbors1: list, genes_to_pass1: list,
                       x, y, hum_int, stage_1, stage_2, stage_3, field_size_x, field_size_y):
        """decides how good cell(x, y) will be dividing
        stage_i - rules of goodness"""
        if hum_int ** 2 <= stage_1 ** 2:
            neighbors1, genes_to_pass1 =  long_neighbors(cell_genes, neighbors1, genes_to_pass1,
                                                        x, y, field_size_x, field_size_y)
        elif hum_int ** 2 <= stage_2 ** 2:
            neighbors1, genes_to_pass1 = muavr_neighbors(cell_genes, neighbors1, genes_to_pass1,
                                                        x, y, field_size_x, field_size_y)
        elif hum_int ** 2 <= stage_3 ** 2:
            neighbors1, genes_to_pass1 = fraun_neighbors(cell_genes, neighbors1, genes_to_pass1,
                                                         x, y, field_size_x, field_size_y)
        return neighbors1, genes_to_pass1
@njit(fastmath=True, cache=True)
def find_rand_mut(gene1, radioactivity, edge_of_inf, max_inf):
    '''calculates parameter for random_mutation'''
    dif = gene1 - radioactivity
    if dif > edge_of_inf:
        rand_mut = 0
    else:
        rand_mut = math.floor(-max_inf / 2 / edge_of_inf * (dif - edge_of_inf))
    return rand_mut, dif
@njit(fastmath=True, cache=True)
def born_survive(genes, live, food, radioactivity, neighbors, neighbors_born, neighbors_exist_start, neighbors_exist_end,
                 max_inf, edge_of_inf, genes_to_pass):
    '''Decides future for cell'''
    # calculating random mutation parameter
    # according to cell_radio-resistance and environment radioactivity
    rand_mut, dif = find_rand_mut(genes[1], radioactivity, edge_of_inf, max_inf)

    if live > 0:
        # if cell has overpopulation or underpopulation
        if neighbors < neighbors_exist_start or neighbors > neighbors_exist_end:
            live -= 5
            if live <= 0:
                genes[0] = 0
                genes[1] = 0
                # drop of food with some chance
                food += 1
        else:
            # Influence of radiation
            if dif < edge_of_inf:
                live -= 2
                if live <= 0:
                    genes[0] = 0
                    genes[1] = 0
            genes[0] += randint(-rand_mut, rand_mut)
            genes[1] += randint(-rand_mut, rand_mut)
            genes[0] = gen_out_of_range(genes[0])
            genes[1] = gen_out_of_range(genes[1])
            # if cell has food on it
            if food > 0:
                food -= 2
    # if dead cell has enough parents
    elif neighbors == neighbors_born:
        if food > 2:
            food -= 2
            live = 5
        # giving parents genes and random mutation(because of reproduction)
        for i in range(len(genes)):
            genes[i] = genes_to_pass[i] / neighbors + randint(-3, 3)
            genes[i] = gen_out_of_range(genes[i])
    if food < 20:
        food += 0.3
    food = gen_out_of_range(food)
    return genes, live, food

def step(Field):
    '''
    Field - class of Field

    Method generate new field by basics rules
    '''


    # Main constants of the game
    # conditions of birth
    neighbors_born = Field.neighbors_born
    neighbors_exist_start = Field.neighbors_exist_start
    neighbors_exist_end = Field.neighbors_exist_end
    # conditions for dividing stages(good and bad genes-environment combinations)
    # the best combination(gives super dividing)
    stage_1 = 10
    # usual combination
    stage_2 = 40
    # bad combination
    stage_3 = 60
    # radiation influence parameter
    max_inf = 20
    edge_of_inf = 10
    # cloud moves
    Field.cloud.clear(Field)
    Field.cloud.move(Field.size_x, Field.size_y)
    Field.cloud.mod(Field)
    # list of number of neighbors around 1 cell
    neighbors = zeros((Field.size_x, Field.size_y))
    # list of sums of genes of life cells around cell and number of life cells
    genes_to_pass = zeros(shape=(Field.size_x, Field.size_y, 2))
    k = time.perf_counter()
    for x in range(Field.size_x):
        for y in range(Field.size_y):
            cell = Field.cells[x][y]
            #counting number of neighbors
            if cell.live > 0:
                # calculating humidity interaction parameter
                # tells how close humidity and corresponding genes are
                hum_int = cell.genes[0] - cell.humidity
                # condition decider, calculates how good cell will divide
                neighbors, genes_to_pass = divide_manager(cell.genes, neighbors,genes_to_pass, x, y, hum_int,
                                stage_1, stage_2, stage_3, Field.size_x, Field.size_y)
    print(time.perf_counter() - k)
    k = time.perf_counter()
    for x in range(Field.size_x):
        for y in range(Field.size_y):
            # Decide if cell will be born, stay the same or die
            cell = Field.cells[x][y]
            cell.genes, cell.live, cell.food = born_survive(cell.genes, cell.live, cell.food, cell.radioactivity, neighbors[x][y],
                             neighbors_born, neighbors_exist_start, neighbors_exist_end,
                             max_inf, edge_of_inf, genes_to_pass[x][y])
            cell.color, cell.color_bg = change_colors(cell.genes, cell.humidity, cell.food, cell.radioactivity)
    print(time.perf_counter() - k)
    return Field
@njit(fastmath=True, cache=True)
def change_colors(genes, humidity, food, radioactivity):
    """changes color of cell and cell_bg according to genes"""
    color = (floor(255 * (genes[1] + 100) / 200),
                    0,
                    floor(255 * (genes[0] + 100) / 200))
    green = math.floor(255 * (food + 100) / 200)
    if green > 255:
        green = 255
    color_bg = (
    ceil(255 * (100 + radioactivity) / 200), green, floor(255 * (100 + humidity) / 200))
    return color, color_bg
def change_scale(field, par):
    """changes scale of field, increases it if par = 1, decreases it if par = -1"""
    change_step = 5
    field.scale += par * change_step
    if field.scale <= 5:
        field.scale = 5


def find_grid(field, game_window):
    """calculates optimal grid size to display it in game_window
    look of grid: (coordinate of top left corner, number of rows and colons, size of 1 cell,
                    (x, y) - coordinates of top left cell)
    game_window - array of coordinates of left upper corner, lenth and height of window"""
    game_window_x_center = game_window[0] + game_window[2] / 2
    game_window_y_center = game_window[1] + game_window[3] / 2
    cell_size = field.scale
    grid = [0, 0, 0, 0, 0, 0]
    # calculating x coordinate of a grid
    dist_x = (game_window_x_center - game_window[0]) / cell_size
    x = field.x_center - dist_x
    X = math.floor(x) - 2
    # calculating y coordinate of a grid in field coors
    dist_y = (game_window_y_center - game_window[1]) / cell_size
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
    grid[0], grid[1] = change_coords(array([X, Y]), cell_size, field.x_center, field.y_center, game_window, 1)
    grid[2] = math.ceil(game_window[2] / cell_size) + 5
    grid[3] = math.ceil(game_window[3] / cell_size) + 5
    if grid[2] + X >= field.size_x:
        grid[2] = field.size_x - X
    if Y - grid[3] <= 0:
        grid[3] = Y + 1
    grid[4] = cell_size
    grid[5] = (X, Y)

    return grid

@njit(fastmath=True, cache=True)
def mouse_pos_check(mouse_pos, rect):
    """checks if mouse is on rect(left up angle, width, height)"""
    if abs(mouse_pos[0] - (rect[0] + rect[2] / 2)) <= rect[2] / 2 and abs(mouse_pos[1] - (rect[1] + rect[3] / 2)) <= \
            rect[3] / 2:
        return True
    else:
        return False

@njit(fastmath=True, cache=True)
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

    x, y = change_coords(array(pos), field.scale, field.x_center, field.y_center, game_window, 0)
    if math.floor(x) >= field.size_x or math.floor(x) < 0 or math.ceil(y) >= field.size_y or math.ceil(y) < 0:
        return None, None
    else:
        return math.floor(x), math.ceil(y)

@njit(fastmath=True, cache=True)
def change_coords(pos: list, cell_size, field_x_center, field_y_center, game_window: list, par_of_change):
    """changes coordinates from field coors to pygame coors
    par of change = 1 if Field coors in pygame, 0 if Pygame coors in field"""
    game_window_x_center = game_window[0] + game_window[2] / 2
    game_window_y_center = game_window[1] + game_window[3] / 2
    if par_of_change == 0:
        x_in_center = pos[0] - game_window_x_center
        y_in_center = pos[1] - game_window_y_center
        x_in_field = x_in_center / cell_size + field_x_center
        y_in_field = - y_in_center / cell_size + field_y_center
        return x_in_field, y_in_field
    elif par_of_change == 1:
        x, y = (pos[0] * cell_size, pos[1] * cell_size)
        X = game_window_x_center + x - field_x_center * cell_size
        Y = game_window_y_center - (y - field_y_center * cell_size)
        return X, Y

def print_text(screen, text: str, text_color, x, y, size, bg_color=None):
    """function that prints given text with pygame
    x,y - coors of text center"""
    font = pygame.font.Font(pygame.font.get_default_font(), size)
    text_rendered = font.render(text, True, text_color, bg_color)
    text_rect = text_rendered.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_rendered, text_rect)


if __name__ == "__main__":
    print("This module is not for direct call!")
