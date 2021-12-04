import math
import pygame
from random import randint


def step(Field):
    '''
    Field - class of Field
    
    Method generate new field by basics rules
    '''

    def muavr_neighbors(field, neighbors, x, y):
        '''Count neighbors in area of nearest 8 cells'''
        for i in range(x - 1, (x + 2) % field.size_x, 1):
            for j in range(y - 1, (y + 2) % field.size_y, 1):
                neighbors[i][j] += 1
                # adding parent gene
                genes_to_pass[i][j][0] += field.cells[x][y].genes[0]
        neighbors[x][y] -= 1
        genes_to_pass[x][y][0] -= field.cells[x][y].genes[0]

    def fraun_neighbors(field, neighbors, x, y):
        '''Count neighbors in 4 bordered cells'''
        neighbors[x - 1][y] += 1
        genes_to_pass[x - 1][y][0] += field.cells[x][y].genes[0]

        neighbors[x][(y + 1) % field.size_y] += 1
        genes_to_pass[x][(y + 1) % field.size_y][0] += field.cells[x][y].genes[0]

        neighbors[x][y - 1] += 1
        genes_to_pass[x][y - 1][0] += field.cells[x][y].genes[0]

        neighbors[(x + 1) % field.size_x][y] += 1
        genes_to_pass[(x + 1) % field.size_x][y][0] += field.cells[x][y].genes[0]

    def long_neighbors(field, neighbors, x, y):
        '''Count neighbors in area of nearest 8 cells and more 4 cells on the distance 2cells away'''
        # closest 8 cells
        for i in range(x - 1, (x + 2) % field.size_x, 1):
            for j in range(y - 1, (y + 2) % field.size_y, 1):
                neighbors[i][j] += 1
                # adding parent gene
                genes_to_pass[i][j][0] += field.cells[x][y].genes[0]
        # additional 4 cells
        neighbors[x - 2][y] += 1
        genes_to_pass[x - 2][y][0] += field.cells[x][y].genes[0]

        neighbors[x][(y + 2) % field.size_y] += 1
        genes_to_pass[x][(y + 2) % field.size_y][0] += field.cells[x][y].genes[0]

        neighbors[x][y - 2] += 1
        genes_to_pass[x][y - 2][0] += field.cells[x][y].genes[0]

        neighbors[(x + 2) % field.size_x][y] += 1
        genes_to_pass[(x + 2) % field.size_x][y][0] += field.cells[x][y].genes[0]

        neighbors[x][y] -= 1
        genes_to_pass[x][y][0] -= field.cells[x][y].genes[0]

    def born_survive(Field, neighbors, x, y):
        '''Shows if cells alives, born or die'''
        # calculating random mutation parameter
        # according to cell_radio-resistance and environment radioactivity
        rand_mut = math.floor((Field.cells[x][y].radioactivity+100+rad_inf)/(Field.cells[x][y].genes[1]+101))
        if Field.cells[x][y].live:
            # if cell has food on it
            #if Field.cells[x][y].food > 0:
            #    Field.cells[x][y].food -= 2
            #    Field.cells[x][y].live += 1
            # if cell has overpopulation or underpopulation
            if neighbors[x][y] < neighbors_exist_start or neighbors[x][y] > neighbors_exist_end:
                Field.cells[x][y].live -= 5
                if Field.cells[x][y].live <= 0:
                    Field.cells[x][y].genes[0] = 0
                    Field.cells[x][y].genes[1] = 0
                    #if randint(0, 10) == 0: #drop of food with some chance
                    #    Field.cells[x][y].food += 1
            else:  # Influence of radiation
                Field.cells[x][y].genes[0] += randint(-rand_mut, rand_mut)
                Field.cells[x][y].genes[1] += randint(-rand_mut, rand_mut)
                Field.cells[x][y].genes[0] = gen_out_of_range(Field.cells[x][y].genes[0])
                Field.cells[x][y].genes[1] = gen_out_of_range(Field.cells[x][y].genes[1])
        # if dead cell has enough parents
        elif neighbors[x][y] == neighbors_born:
            Field.cells[x][y].live = 5
            # giving parents genes and random mutation(because of reproduction)
            for i in range(len(Field.cells[x][y].genes)):
                Field.cells[x][y].genes[i] = genes_to_pass[x][y][i] / neighbors[x][y] + randint(-3, 3)
                Field.cells[x][y].genes[i] = gen_out_of_range(Field.cells[x][y].genes[i])
    def divide_manager(Field, neighbors, x, y, hum_int, stage_1, stage_2, stage_3):
        """decides how good cell(x, y) will be dividing
        stage_i - rules of goodness"""
        if hum_int ** 2 <= stage_1 ** 2:
            long_neighbors(Field, neighbors, x, y)
        elif hum_int ** 2 <= stage_2 ** 2:
            muavr_neighbors(Field, neighbors, x, y)
        elif hum_int ** 2 <= stage_3 ** 2:
            fraun_neighbors(Field, neighbors, x, y)

    def gen_out_of_range(gen):
        """checks if gen is in -100 to 100 range, else changes it"""
        if gen > 100:
            gen = 100
        elif gen < -100:
            gen = -100
        return gen

    # Main constants of the game
    # conditions of birth
    neighbors_born = 3
    neighbors_exist_start = 2
    neighbors_exist_end = 3
    # conditions for dividing stages(good and bad genes-environment combinations)
    # the best combination(gives super dividing)
    stage_1 = 3
    # usual combination
    stage_2 = 30
    # bad combination
    stage_3 = 50
    # radiation influence parameter
    rad_inf = 20
    # list of number of neighbors around 1 cell
    neighbors = [[0] * Field.size_y for i in range(Field.size_x)]
    # list of sums of genes of life cells around cell and number of life cells
    genes_to_pass = [[[0, 0] for j in range(Field.size_y)] for i in range(Field.size_x)]
    for x in range(0, Field.size_x, 1):
        for y in range(0, Field.size_y, 1):
            # counting number of neighbors
            if Field.cells[x][y].live:
                # calculating humidity interaction parameter
                # tells how close humidity and corresponding genes are
                hum_int = Field.cells[x][y].genes[0] - Field.cells[x][y].humidity
                # condition decider, calculates how good cell will divide
                divide_manager(Field, neighbors, x, y, hum_int, stage_1, stage_2, stage_3)

    for x in range(0, Field.size_x, 1):
        for y in range(0, Field.size_y, 1):
            # Decide if cell born, exist or die
            born_survive(Field, neighbors, x, y)
            Field.cells[x][y].change_colors()


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
    grid[0], grid[1] = change_coords((X, Y), cell_size, field.x_center, field.y_center, game_window, 1)
    grid[2] = math.ceil(game_window[2] / cell_size) + 5
    grid[3] = math.ceil(game_window[3] / cell_size) + 5
    if grid[2] + X >= field.size_x:
        grid[2] = field.size_x - X
    if Y - grid[3] <= 0:
        grid[3] = Y + 1
    grid[4] = cell_size
    grid[5] = (X, Y)

    return grid


def mouse_pos_check(mouse_pos, rect):
    """checks if mouse is on rect(left up angle, width, height)"""
    if abs(mouse_pos[0] - (rect[0] + rect[2] / 2)) <= rect[2] / 2 and abs(mouse_pos[1] - (rect[1] + rect[3] / 2)) <= \
            rect[3] / 2:
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
    if math.floor(x) >= field.size_x or math.floor(x) < 0 or math.ceil(y) >= field.size_y or math.ceil(y) < 0:
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
        x_in_field = x_in_center / cell_size + field_x_center
        y_in_field = - y_in_center / cell_size + field_y_center
        return x_in_field, y_in_field
    elif par_of_change == 1:
        x, y = (pos[0] * cell_size, pos[1] * cell_size)
        X = game_window_x_center + x - field_x_center * cell_size
        Y = game_window_y_center - (y - field_y_center * cell_size)
        return X, Y


def print_text(screen, text: str, text_color, x, y, size):
    """function that prints given text with pygame
    x,y - coors of text center"""
    font = pygame.font.Font(pygame.font.get_default_font(), size)
    text_rendered = font.render(text, True, text_color)
    text_rect = text_rendered.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_rendered, text_rect)


if __name__ == "__main__":
    print("This module is not for direct call!")
