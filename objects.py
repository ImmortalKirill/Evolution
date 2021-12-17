from random import randint
import pygame
import pygame.freetype
import math
from model import saving, upload
from pygame.draw import *
from collections import deque
from numpy import array, zeros
from numba import njit
from numba.experimental import jitclass


class Cell:
    """ class of one cell on a Field"""

    def __init__(self):
        self.live = 0
        self.x = 0
        self.y = 0
        self.color = (255, 255, 255)
        self.color_bg = (0, 0, 0)
        self.genes = array([0, 0])
        self.humidity = 0
        # radioactive resistance
        self.radioactivity = -100
        self.food = 0

    def new_cell(self, x0, y0):
        x = self.x = x0
        y = self.y = y0


class Cloud:
    """
    Create cloud with parametrs:
    cells - information about radiation
    size_x, size_y - sizes of cloud
    x, y - coordinates of left upper cornor
    speed_x, speed_y - speed of cloud
    count - periodic of changing speed
    time - self time of cloud
    slow - how often cloud moves
    """

    def __init__(self, x, y, slow):
        size_x = self.size_x = x
        size_y = self.size_y = y
        cells = self.cells = [[0] * size_x for i in range(size_y)]
        x = self.x = 0
        y = self.y = 0
        speed_x = self.speed_x = 1
        speed_y = self.speed_y = 1
        count = self.count = 0
        time = self.time = 0
        self.slow = slow
        self.old_cells = zeros((self.size_x, self.size_y))

    def new_cloud(self):
        self.cells = [[0] * self.size_x for i in range(self.size_y)]
        for i in range(self.size_x):
            for j in range(self.size_y):
                self.cells[i][j] = math.floor((self.size_x * self.size_y / 4 - abs((i - self.size_x / 2) * (j - self.size_y / 2))) 
                                         / (self.size_x * self.size_y / 4) * 200 - 100)

    def move(self, size_x, size_y):
        self.x = (self.x + self.speed_x) % size_x
        self.y = (self.y + self.speed_y) % size_y
        self.count += 1
        if self.count % 20 == 0:
            self.speed_x = randint(-2, 3)
            self.speed_y = randint(-2, 3)

    def mod(self, field):
        # modified field
        for i in range(self.size_x):
            for j in range(self.size_y):
                temp = field.cells[(self.x + i) % field.size_x][(self.y + j) % field.size_y].radioactivity
                self.old_cells[i][j] = temp
                temp2 = self.cells[i][j] + temp
                if temp2 > field.cells[(self.x + i) % field.size_x][(self.y + j) % field.size_y].radioactivity:
                    field.cells[(self.x + i) % field.size_x][(self.y + j) % field.size_y].radioactivity = min(temp2, 100)

    def clear(self, field):
        # clear itself
        field_x = field.size_x
        field_y = field.size_y
        for i in range(self.size_x):
            for j in range(self.size_y):
                field.cells[(self.x + i) % field_x][(self.y + j) % field_y].radioactivity = self.old_cells[i][j]


class Button:
    """class of buttons"""

    def __init__(self, bg_rect: list, text_color, text, bg_color=(230, 230, 250), text_pressed='', angle=0, size=24):
        """x,y - coordinates of left top corner
        color - color of bottom
        text - text on the bottom
        bg_rect = list [x, y, width, height] where x,y - coordinates of left top angle of rect of background
        text_rect = list [x, y, width, height] where x,y - coordinates of left top angle of rect of text"""
        # self.x = x
        # self.y = y
        # self.height = height
        # self.width = width
        self.text_color = text_color
        self.text = text
        self.bg_color = bg_color
        self.bg_rect = array(bg_rect)
        self.text_rect = array([0, 0, 0, 0])
        self.angle = angle
        self.size = size
        # pressed = 0 if not pressed and 1 if pressed
        self.pressed = 0
        self.pressed_color = (100, 100, 120)
        self.text_pressed = text_pressed

    def draw(self, screen):
        """draws button with text on the screen"""

        font = pygame.freetype.SysFont(pygame.freetype.get_default_font(), self.size)

        if self.pressed == 0:
            rect(screen, self.bg_color, self.bg_rect)
            if self.text == '+':
                print_text(screen, self.text, self.text_color, self.bg_rect[0] + self.bg_rect[2] / 2, self.bg_rect[1] +
                           self.bg_rect[3] / 2 - 3, self.size, self.bg_color)
            else:
                print_text(screen, self.text, self.text_color, self.bg_rect[0] + self.bg_rect[2] / 2, self.bg_rect[1] +
                           self.bg_rect[3] / 2, self.size, self.bg_color)

        else:
            rect(screen, self.pressed_color, self.bg_rect)
            if (self.text_pressed == '+') or (self.text_pressed == '>'):
                print_text(screen, self.text_pressed, (255, 255, 255), self.bg_rect[0] + self.bg_rect[2] / 2,
                           self.bg_rect[1] +
                           self.bg_rect[3] / 2 - 3, self.size, self.pressed_color)
            else:
                print_text(screen, self.text_pressed, (255, 255, 255), self.bg_rect[0] + self.bg_rect[2] / 2,
                           self.bg_rect[1] + self.bg_rect[3] / 2, self.size, self.pressed_color)

        text_rect_fig = pygame.freetype.Font.get_rect(font, self.text, size=self.size)

        self.text_rect[0] = text_rect_fig.left
        self.text_rect[1] = text_rect_fig.top
        self.text_rect[2] = text_rect_fig.width
        self.text_rect[3] = text_rect_fig.height

    def change_press(self):
        """changes state of button"""
        self.pressed += 1
        self.pressed = self.pressed % 2

from model import mouse_pos_check, print_text, change_coords, change_colors


class Slider(Button):
    """class of sliders that can change some parameter smoothly"""
    def __init__(self, bg_rect, text_color=(0, 0, 0), text='Parameter', bg_color=(0, 0, 0), text_pressed='', angle=0,
                 upper_value: int = 10, current_value_points: int = 30, minus_value=0):
        """position - tuple of left top angle coors of slider - (x, y)
        upper_value - maximum value that parameter can reach
        current_value_points - value on slider in points of pygame
        text - name of changed parameter
        outline_size - tuple of width and height of the slider
        """
        super().__init__(bg_rect, text_color, text, bg_color, text_pressed, angle)
        self.current_value_points = current_value_points
        self.upper_value = upper_value
        self.font = 0
        self.minus_value = minus_value
        self.scale = self.bg_rect[2] / self.upper_value

    # returns the current value of the slider
    def get_value(self) -> float:
        """function gives rounded value of slider's parameter"""
        return round(self.current_value_points / self.scale - self.minus_value)

    # renders slider and the text showing the value of the slider
    def draw(self, screen: pygame.display):
        """ draws slider on the screen"""
        # draw outline and slider rectangles
        pygame.draw.rect(screen, self.bg_color, (self.bg_rect[0], self.bg_rect[1],
                                                 self.bg_rect[2], self.bg_rect[3]), 1)

        pygame.draw.rect(screen, self.bg_color, (self.bg_rect[0], self.bg_rect[1],
                                                 self.current_value_points, self.bg_rect[3] - 3))

        print_text(screen, f"{self.text}: {self.get_value()}", self.text_color, self.bg_rect[0] + (self.bg_rect[2] / 2),
                   self.bg_rect[1] + self.bg_rect[3] * 1.5, int(self.bg_rect[3] / 2))

    def change_value(self):
        """allows users to change value of the slider by dragging it"""
        # If mouse is pressed and mouse is inside the slider
        mouse_pos = pygame.mouse.get_pos()
        if mouse_pos_check(array(mouse_pos), self.bg_rect):
            # the size of the slider
            self.current_value_points = mouse_pos[0] - self.bg_rect[0]

            # limit the size of the slider
            if self.current_value_points < 1:
                self.current_value_points = 0
            if self.current_value_points > self.bg_rect[2]:
                self.current_value_points = self.bg_rect[2]


class Interface:
    """creates class with all buttons and sliders in the bottom part of window"""

    def __init__(self, width, height, game_window):
        """WIDTH, HEIGHT - size of the app window"""
        self.game_window = game_window
        self.WIDTH = width
        self.HEIGHT = height
        # Buttons of Interface
        self.clear = Button([600, 710, 50, 30], (0, 0, 0), 'clear', text_pressed='0', size=16)
        self.pause = Button([10, 710, 30, 30], (0, 0, 0), 'II', text_pressed='>', angle=90)
        self.cell_spawn = Button([50, 710, 30, 30], (0, 0, 0), '+', text_pressed='+', size=24)
        self.population_spawn = Button([100, 710, 80, 30], (0, 0, 0), 'new field', text_pressed='new field', size=16)
        self.slider = Slider(bg_rect=[200, 710, 300, 30], text='speed')
        self.background_color = (129, 129, 144)
        self.save = Button([700, 710, 50, 30], (0, 0, 0), 'save', text_pressed='accept', size=16)
        self.upload = Button([760, 710, 60, 30], (0, 0, 0), 'upload', text_pressed='accept', size=16)
        self.name_of_file = ''
        self.font = pygame.font.Font(None, 30)

    def draw(self, screen):
        """draws interface on the screen"""
        # drawing interface background
        # top rect
        pygame.draw.rect(screen, self.background_color, [0, 0, self.WIDTH, self.game_window[1]], 0)
        # left rect
        pygame.draw.rect(screen, self.background_color, [0, 0, self.game_window[0], self.HEIGHT], 0)
        # down rect
        pygame.draw.rect(screen, self.background_color, [0, self.game_window[1] + self.game_window[3],
                                                         self.WIDTH,
                                                         self.HEIGHT - self.game_window[1] - self.game_window[3]], 0
                         )
        # right rect
        pygame.draw.rect(screen, self.background_color, [self.game_window[0] + self.game_window[2], 0,
                                                         self.WIDTH - self.game_window[0] - self.game_window[2],
                                                         self.HEIGHT], 0
                         )
        # drawing buttons
        self.pause.draw(screen)
        self.cell_spawn.draw(screen)
        self.slider.draw(screen)
        self.clear.draw(screen)
        self.population_spawn.draw(screen)
        self.save.draw(screen)
        self.upload.draw(screen)
        
        text = self.font.render(self.name_of_file, True, (0, 0, 0))
        screen.blit(text, (720, 760))


class Settings(Interface):
    """creates class of additional menu that controls pen and cell and field settings"""

    def __init__(self, width, height, game_window, game_window_width, status,
                 indent=100, slider_width=150):
        super().__init__(width, height, game_window)
        self.font = 0
        self.width = width
        self.slider_width = slider_width
        # is settings activated
        self.status = status
        # headers text
        self.field_text = 'Field'
        self.cell_text = 'Cell'
        self.text_color = 'black'
        self.game_window_width = game_window_width
        self.cell = Cell()
        self.cell_pen = Cell()
        self.pen_rect = (0, 0, 0, 0)
        self.indent = indent
        self.background_color = (129, 129, 144)
        # sliders
        self.field_humidity_slider = Slider(bg_rect=[self.game_window[0] + self.game_window[2] +
                                                     (self.width - self.slider_width) / 2, indent - 25,
                                                     self.slider_width, 30],
                                            text='humidity', upper_value=200, minus_value=100)
        self.field_radioactivity_slider = Slider(
            bg_rect=[self.game_window[0] + self.game_window[2] + (self.width - self.slider_width) / 2, 2 * indent - 25,
                     self.slider_width, 30], text='radioactivity', upper_value=200, minus_value=100)
        self.field_food_slider = Slider(
            bg_rect=[self.game_window[0] + self.game_window[2] + (self.width - self.slider_width) / 2, 3 * indent - 25,
                     self.slider_width, 30], text='food', upper_value=200, minus_value=100)
        self.cell_humidity_slider = Slider(
            bg_rect=[self.game_window[0] + self.game_window[2] + (self.width - self.slider_width) / 2, 4 * indent,
                     self.slider_width, 30], text='humidity', upper_value=200, minus_value=100)
        self.cell_radioactivity_slider = Slider(
            bg_rect=[self.game_window[0] + self.game_window[2] + (self.width - self.slider_width) / 2, 5 * indent,
                     self.slider_width, 30], text='radioactivity', upper_value=200, minus_value=100)
        self.pen_radius = Slider(
            bg_rect=[self.game_window[0] + self.game_window[2] + (self.width - self.slider_width) / 2, 6.5 * indent,
                     self.slider_width, 30], text='pen radius', upper_value=10, minus_value=0)
        # buttons
        self.pen = Button([self.game_window[0] + self.game_window[2] + 10, 6 * indent, 40, 30], (0, 0, 0), 'pen',
                          text_pressed='pen', angle=0, size=16)
        self.cell_button = Button([self.game_window[0] + self.game_window[2] + 60, 6 * indent, 40, 30], (0, 0, 0),
                                  'cell', text_pressed='cell', size=16)
        self.field_button = Button([self.game_window[0] + self.game_window[2] + 110, 6 * indent, 40, 30], (0, 0, 0),
                                   'field', text_pressed='field', size=16)

    def draw(self, screen):
        """ draws settings on the screen if it is activated (button + is pressed)"""
        if (self.status % 2) == 1:

            self.game_window[2] = self.game_window_width - self.width
            pygame.draw.rect(screen, self.background_color, [self.game_window[0] + self.game_window[2], 0,
                                                             self.WIDTH + self.game_window[0] + self.game_window[2],
                                                             self.HEIGHT], 0)
            self.field_humidity_slider.draw(screen)
            self.field_radioactivity_slider.draw(screen)
            self.field_food_slider.draw(screen)
            self.cell_humidity_slider.draw(screen)
            self.cell_radioactivity_slider.draw(screen)
            self.pen_radius.draw(screen)

            # examples of colors near of sliders
            # field humidity
            pygame.draw.rect(screen, (0, 0, 0),
                             [self.game_window[0] + self.game_window[2] + 10, self.indent - 25, 5, 30])
            pygame.draw.rect(screen, (0, 0, 255), [self.game_window[0] + self.game_window[2] + self.WIDTH - 15,
                                                   self.indent - 25, 5, 30])
            # field radioactivity
            pygame.draw.rect(screen, (0, 0, 0),
                             [self.game_window[0] + self.game_window[2] + 10, 2 * self.indent - 25, 5, 30])
            pygame.draw.rect(screen, (255, 0, 0), [self.game_window[0] + self.game_window[2] + self.WIDTH - 15,
                                                   2 * self.indent - 25, 5, 30])
            # field food
            pygame.draw.rect(screen, (0, 0, 0),
                             [self.game_window[0] + self.game_window[2] + 10, 3 * self.indent - 25, 5, 30])
            pygame.draw.rect(screen, (0, 255, 0), [self.game_window[0] + self.game_window[2] + self.WIDTH - 15,
                                                   3 * self.indent - 25, 5, 30])

            # cell humidity
            pygame.draw.rect(screen, (0, 0, 0),
                             [self.game_window[0] + self.game_window[2] + 10, 4 * self.indent, 5, 30])
            pygame.draw.rect(screen, (0, 0, 255), [self.game_window[0] + self.game_window[2] + self.WIDTH - 15,
                                                   4 * self.indent, 5, 30])
            # cell radioactivity
            pygame.draw.rect(screen, (0, 0, 0),
                             [self.game_window[0] + self.game_window[2] + 10, 5 * self.indent, 5, 30])
            pygame.draw.rect(screen, (255, 0, 0), [self.game_window[0] + self.game_window[2] + self.WIDTH - 15,
                                                   5 * self.indent, 5, 30])

            # printing heads
            print_text(screen, self.field_text, self.text_color, self.game_window[0] + self.game_window[2] + 100, 50,
                       18)
            print_text(screen, self.cell_text, self.text_color, self.game_window[0] + self.game_window[2] + 100,
                       self.indent * 3.75, 18)

            # drawing rect that shows pen area
            self.pen.draw(screen)
            if self.pen.pressed:
                self.cell_button.draw(screen)
                self.field_button.draw(screen)
        else:
            self.game_window[2] = self.game_window_width

    def draw_pen_rect(self, screen):
        """ draws red square with pen_rect coors - pen area"""
        if self.pen.pressed:
            pygame.draw.rect(screen, 'red', self.pen_rect, 4)

    def update(self):
        """changes values of cells and field in settings"""

        self.pen_radius.change_value()

        if (not self.pen.pressed) or self.field_button.pressed:
            self.field_humidity_slider.change_value()
            self.cell.humidity = self.field_humidity_slider.get_value()

            self.field_radioactivity_slider.change_value()
            self.cell.radioactivity = self.field_radioactivity_slider.get_value()

            self.field_food_slider.change_value()
            self.cell.food = self.field_food_slider.get_value()

        if (not self.pen.pressed) or self.cell_button.pressed:
            self.cell_humidity_slider.change_value()
            self.cell.genes[0] = self.cell_humidity_slider.get_value()

            self.cell_radioactivity_slider.change_value()
            self.cell.genes[1] = self.cell_radioactivity_slider.get_value()

        self.cell.color, self.cell.color_bg = change_colors(self.cell.genes, self.cell.humidity, self.cell.food,
                                                            self.cell.radioactivity)

    def update_slider(self):
        """ gets parameters of cells and field when pen is not activated"""

        self.field_humidity_slider.current_value_points = (self.cell.humidity + self.field_humidity_slider.minus_value) \
                                                          * self.field_humidity_slider.scale

        self.field_radioactivity_slider.current_value_points = (self.cell.radioactivity
                                                                + self.field_radioactivity_slider.minus_value) \
                                                               * self.field_radioactivity_slider.scale

        self.field_food_slider.current_value_points = (self.cell.food
                                                       + self.field_food_slider.minus_value) \
                                                      * self.field_food_slider.scale

        self.cell_humidity_slider.current_value_points = (self.cell.genes[0] + self.cell_humidity_slider.minus_value) \
                                                         * self.cell_humidity_slider.scale
        self.cell_radioactivity_slider.current_value_points = (self.cell.genes[
                                                                   1] + self.cell_radioactivity_slider.minus_value) \
                                                              * self.cell_radioactivity_slider.scale

    def redraw(self):
        """ draws new cells with given parameters with pen"""
        if self.pen.pressed:
            if self.cell_button.pressed:
                self.cell_humidity_slider.change_value()
                self.cell.genes[0] = self.cell_humidity_slider.get_value()

                self.cell_radioactivity_slider.change_value()
                self.cell.genes[1] = self.cell_radioactivity_slider.get_value()

                self.cell.color, self.cell.color_bg = change_colors(self.cell.genes, self.cell.humidity, self.cell.food,
                                                                    self.cell.radioactivity)
            if self.field_button.pressed:
                self.field_humidity_slider.change_value()
                self.cell.humidity = self.field_humidity_slider.get_value()

                self.field_radioactivity_slider.change_value()
                self.cell.radioactivity = self.field_radioactivity_slider.get_value()

                self.field_food_slider.change_value()
                self.cell.food = self.field_food_slider.get_value()

                self.cell.color, self.cell.color_bg = change_colors(self.cell.genes, self.cell.humidity, self.cell.food,
                                                                    self.cell.radioactivity)


class Menu(Interface):
    """ class of all buttons and text - main menu that introduce our game"""
    def __init__(self, width, height, game_window):
        super().__init__(width, height, game_window)
        self.width = width
        self.height = height
        self.bg_color = (200, 200, 200)
        self.rect_color = (100, 100, 100)
        self.text_color = (0, 0, 0)
        self.last = pygame.time.get_ticks()
        # buttons
        self.start = Button([7.5 * width / 10, 7 * height / 10, width / 10, height / 20], (0, 0, 0), 'start',
                            bg_color=(255, 255, 255),
                            text_pressed='start', size=24)
        # buttons to choose field size
        self.small_field = Button([6.15 * width / 10, 3 * height / 10, width / 10, height / 20], (0, 0, 0), 'small',
                                  bg_color=(255, 255, 255), text_pressed='small', size=20)
        self.middle_field = Button([7.25 * width / 10, 3 * height / 10, width / 10, height / 20], (0, 0, 0), 'middle',
                                   bg_color=(255, 255, 255),
                                   text_pressed='middle', size=20)
        self.large_field = Button([8.35 * width / 10, 3 * height / 10, width / 10, height / 20], (0, 0, 0), 'large',
                                  bg_color=(255, 255, 255),
                                  text_pressed='large', size=20)

    def draw(self, screen):
        """ draws menu on the screen"""
        screen.fill(self.bg_color)
        print_text(screen, 'Evolution', self.text_color, self.width / 2, self.height / 10, 46)
        # block of rules
        pygame.draw.rect(screen, self.rect_color,
                         (self.width / 20, 2 * self.height / 10, self.width / 2, 6 * self.height / 10))
        # block of window settings
        pygame.draw.rect(screen, self.rect_color,
                         (6 * self.width / 10, 2 * self.height / 10, 3.5 * self.width / 10, 3 * self.height / 10))
        # text
        print_text(screen, 'Rules', self.text_color, 11 * self.width / 40, 2.5 * self.height / 10, 32)
        print_text(screen, 'Choose window size:', self.text_color, 15.5 * self.width / 20, 2.5 * self.height / 10, 28)
        # buttons
        self.start.draw(screen)
        self.small_field.draw(screen)
        self.middle_field.draw(screen)
        self.large_field.draw(screen)


class Field:
    """ class Field, consists of cells"""

    def __init__(self):
        cells = self.cells = [[]]
        x_center = self.x_center = 0
        y_center = self.y_center = 0
        scale = self.scale = 50
        size_x = self.size_x = 0
        size_y = self.size_y = 0
        neighbors_born = self.neighbors_born = 3
        neighbors_exist_start = self.neighbors_exist_start = 2
        neighbors_exist_end = self.neighbors_exist_end = 3
        cloud = self.cloud = Cloud(33, 33, 3)
        # live_cells = self.live_cells = []

    def new_field(self, x, y):
        """ creates new field with size x:y cells"""
        self.cells = [[0] * y for l in range(x)]
        self.size_x = x
        self.size_y = y

        def midpoint_displacement(x, upper_point, bottom_point, sharpest):
            size = x
            heightmap = [[0]*size for i in range(size)]
    
            heightmap[0][0] = randint(bottom_point, upper_point)
            heightmap[size - 1][0] = randint(bottom_point, upper_point)
            heightmap[0][size - 1] = randint(bottom_point, upper_point)
            heightmap[size - 1][size - 1] = randint(bottom_point, upper_point)
    
            q = deque()
            q.append((0, 0, size - 1, size - 1, sharpest))
    
            while len(q) != 0:
                top, left, bottom, right, randomness = q.popleft()
    
                centerX = (left + right) // 2
                centerY = (top + bottom) // 2
    
                heightmap[centerX][top] = (heightmap[left][top] + heightmap[right][top]) // 2 + randint(-randomness, randomness)
                heightmap[centerX][bottom] = (heightmap[left][bottom] + heightmap[right][bottom]) // 2 + randint(-randomness, randomness)
                heightmap[left][centerY] = (heightmap[left][top] + heightmap[left][bottom]) // 2 + randint(-randomness, randomness)
                heightmap[right][centerY] = (heightmap[right][top] + heightmap[right][bottom]) // 2 + randint(-randomness, randomness)
    
                heightmap[centerX][centerY] = (heightmap[left][top] +
                                                   heightmap[right][top] +
                                                   heightmap[left][bottom] +
                                                   heightmap[right][bottom]) // 4 + \
                        randint(-randomness, randomness)
    
                if right - left > 2:
                    q.append((top, left, centerY, centerX, randomness // 2))
                    q.append((top, centerX, centerY, right, randomness // 2))
                    q.append((centerY, left, bottom, centerX, randomness // 2))
                    q.append((centerY, centerX, bottom, right, randomness // 2))
            return heightmap

        # cloud generation
        massive = midpoint_displacement(self.cloud.size_x, -90, -100, 700)
        for i in range(self.cloud.size_x):
            for j in range(self.cloud.size_y):
                if self.cloud.cells[i][j] > 0:
                    self.cloud.cells[i][j] = min(massive[i][j], 100)
                else:
                    self.cloud.cells[i][j] = max(massive[i][j], -100)

        def generate_field(cells:list, x, y):
            """generates field initial conditions"""
            for i in range(x):
                for l in range(y):
                    cells[i][l] = Cell()
                    cells[i][l].new_cell(i, l)
                    cells[i][l].radioactivity = -90
                    cells[i][l].food = 30
                    if randint(0, 1):
                        cells[i][l].live = 5
                        cells[i][l].genes[0] = -100
                        cells[i][l].genes[1] = 50

            # generate humidity
            massive = midpoint_displacement(x, 100, -100, 200)
            for i in range(x):
                for j in range(y):
                    if massive[i][j] > 0:
                        self.cells[i][j].humidity = min(massive[i][j], 100)
                    else:
                        self.cells[i][j].humidity = max(massive[i][j], -100)
            # generate radioactivity
            self.cloud.mod(self)
        generate_field(self.cells, x, y)
        self.x_center = x / 2
        self.y_center = y / 2
        self.size_x = x
        self.size_y = y

    def change_cors(self, vector):
        """shift of center coordinates on vector(x, y)"""
        self.x_center += vector[0]
        self.y_center += vector[1]


if __name__ == "__main__":
    print("This module is not for direct call!")
