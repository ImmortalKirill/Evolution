from random import randint
import pygame
import pygame.freetype
import math
from pygame.draw import *
from collections import deque


class Cell:
    """ class of one cell on a Field"""

    def __init__(self):
        live = self.live = 0
        x = self.x = 0
        y = self.y = 0
        self.color = (255, 255, 255)
        self.color_bg = (0, 0, 0)
        self.genes = [0, 0]
        self.humidity = 0
        # radioactive resistance
        self.radioactivity = -100
        self.food = 0

    def new_cell(self, x0, y0):
        x = self.x = x0
        y = self.y = y0
        self.change_colors()

    def change_colors(self):
        """changes color of cell and cell_bg according to genes"""
        self.color = (math.floor(255 * (self.genes[1] + 100) / 200),
                      0,
                      math.floor(255 * (self.genes[0] + 100) / 200))
        self.color_bg = (
        math.floor(255 * (100 + self.radioactivity) / 200), 0, math.floor(255 * (100 + self.humidity) / 200))
        
        
        
class Cloud:
    
    def __init__(self, x, y):
        cells = [[]]
        size_x = self.size_x = x
        size_y = self.size_y = y
        x = self.x = 0
        y = self.y = 0
        speed_x = self.speed_x = 1
        speed_y = self.speed_y = 1
        count = self.count = 0
        
        
    def move(self, size_x, size_y):
        self.x = (self.x + self.speed_x) % size_x
        self.y = (self.y + self.speed_y) % size_y
        self.count += 1
        if self.count % 20 == 0:
            self.speed_x = randint(-2, 3)
            self.speed_y = randint(-2, 3)
        
    def mod(self, field):
        #modified field
        field_x = field.size_x
        field_y = field.size_y
        for i in range(self.size_x):
            for j in range(self.size_y):
                field.cells[(self.x + i) % field_x][(self.y + j) % field_y].radioactivity = self.cells[i][j]
                
                
    def clear(self, field):
        #clear itself
        field_x = field.size_x
        field_y = field.size_y
        for i in range(self.size_x):
            for j in range(self.size_y):
                field.cells[(self.x + i) % field_x][(self.y + j) % field_y].radioactivity = -100       


class Button:
    """class of buttons"""

    def __init__(self, bg_rect: list, text_color, bg_color, text, text_pressed='', angle=0):
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
        self.bg_rect = bg_rect
        self.text_rect = [0, 0, 0, 0]
        self.angle = angle
        # pressed = 0 if not pressed and 1 if pressed
        self.pressed = 0
        self.pressed_color = (200, 200, 200)
        self.text_pressed = text_pressed

    def draw(self, screen):
        """draws button with text on the screen"""
        rect(screen, self.bg_color, self.bg_rect)

        font = pygame.freetype.SysFont("Arial", 10)  # FIXME text

        if (self.pressed == 0) or (self.text_pressed == '0'):
            font.render_to(screen, (self.bg_rect[0] + 5, self.bg_rect[1] + 5), self.text, fgcolor=self.text_color,
                           bgcolor=self.bg_color, rotation=self.angle, size=24)
        else:
            font.render_to(screen, (self.bg_rect[0] + 5, self.bg_rect[1] + 5), self.text_pressed,
                           fgcolor=self.text_color, bgcolor=self.pressed_color, size=24)

        text_rect_fig = pygame.freetype.Font.get_rect(font, self.text, size=24)

        self.text_rect[0] = text_rect_fig.left
        self.text_rect[1] = text_rect_fig.top
        self.text_rect[2] = text_rect_fig.width
        self.text_rect[3] = text_rect_fig.height

    def change_press(self):
        """changes state of button"""
        self.pressed += 1
        self.pressed = self.pressed % 2


from model import mouse_pos_check, print_text


class Slider(Button):
    def __init__(self, bg_rect, text_color=(0, 0, 0), bg_color=(0, 0, 0), text='Parameter', text_pressed='', angle=0,
                 upper_value: int = 10, current_value_points: int = 30, minus_value=0):
        """position - tuple of left top angle coors of slider - (x, y)
        upper_value - maximum value that parameter can reach
        current_value_points - value on slider in points of pygame
        text - name of changed parameter
        outline_size - tuple of width and height of the slider
        """
        super().__init__(bg_rect, text_color, bg_color, text, text_pressed, angle)
        self.current_value_points = current_value_points
        self.upper_value = upper_value
        self.font = 0
        self.minus_value = minus_value
        self.scale = self.bg_rect[2] / self.upper_value

    # returns the current value of the slider
    def get_value(self) -> float:
        return round(self.current_value_points / self.scale - self.minus_value)

    # renders slider and the text showing the value of the slider
    def draw(self, screen: pygame.display) -> None:
        # draw outline and slider rectangles
        pygame.draw.rect(screen, self.bg_color, (self.bg_rect[0], self.bg_rect[1],
                                                 self.bg_rect[2], self.bg_rect[3]), 1)

        pygame.draw.rect(screen, self.bg_color, (self.bg_rect[0], self.bg_rect[1],
                                                 self.current_value_points, self.bg_rect[3] - 3))

        print_text(screen, f"{self.text}: {self.get_value()}", self.text_color, self.bg_rect[0] + (self.bg_rect[2] / 2),
                   self.bg_rect[1] + self.bg_rect[3]*1.5, int(self.bg_rect[3]/2))

    # allows users to change value of the slider by dragging it.
    def change_value(self) -> None:
        # If mouse is pressed and mouse is inside the slider
        mousePos = pygame.mouse.get_pos()
        if mouse_pos_check(mousePos, self.bg_rect):
            # the size of the slider
            self.current_value_points = mousePos[0] - self.bg_rect[0]

            # limit the size of the slider
            if self.current_value_points < 1:
                self.current_value_points = 0
            if self.current_value_points > self.bg_rect[2]:
                self.current_value_points = self.bg_rect[2]


class Interface:
    """creates class with all buttons"""

    def __init__(self, width, height, game_window):
        """WIDTH, HEIGHT - size of the game"""
        self.game_window = game_window
        self.WIDTH = width
        self.HEIGHT = height
        # Buttons of Interface
        # FixME This should be a real button with position
        self.clear = Button([600, 700, 30, 30], (0, 0, 0), (255, 255, 255), '0', '0')
        self.pause = Button([0, 700, 30, 30], (0, 0, 0), (255, 255, 255), '=', '>', 90)
        self.cell_spawn = Button([50, 700, 30, 30], (0, 0, 0), (255, 255, 255), '+', '+')
        self.population_spawn = Button([100, 700, 30, 30], (0, 0, 0), (255, 255, 255), '+!', '+!')
        self.button_born = Button([150, 700, 30, 30], (0, 0, 0), (255, 255, 255), '-', '-')
        self.slider = Slider(bg_rect=[200, 700, 300, 30], text='speed')
        self.background_color = (100, 100, 100)


    def draw(self, screen):
        """draws interface"""
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
        self.button_born.draw(screen)


class Settings(Interface):
    """creates class of additional menu with buttons"""

    def __init__(self, width, height, game_window, game_window_width, status, indent=100):
        super().__init__(width, height, game_window)
        self.background_color = (100, 100, 100)
        self.field_humidity_slider = Slider(bg_rect=[self.game_window[0] + self.game_window[2] + 10, indent, 150, 30],
                                            text='humidity', upper_value=200, minus_value=100)
        self.field_radioactivity_slider = Slider(bg_rect=[self.game_window[0] + self.game_window[2] + 10, 2*indent, 150, 30],
                                                 text='radioactivity', upper_value=200, minus_value=100)
        self.cell_humidity_slider = Slider(bg_rect=[self.game_window[0] + self.game_window[2] + 10, 4*indent, 150, 30],
                                            text='humidity', upper_value=200, minus_value=100)
        self.cell_radioactivity_slider = Slider(bg_rect=[self.game_window[0] + self.game_window[2] + 10, 5*indent, 150, 30],
                                                 text='radioactivity', upper_value=200, minus_value=100)
        self.font = 0
        self.width = width
        self.status = status
        self.field_text = 'Field'
        self.cell_text = 'Cell'
        self.text_color = 'black'
        self.game_window_width = game_window_width
        self.cell = Cell()

    def draw(self, screen):
        if (self.status % 2) == 1:
            self.game_window[2] = self.game_window_width - self.width
            pygame.draw.rect(screen, self.background_color, [self.game_window[0] + self.game_window[2], 0,
                                                             self.WIDTH + self.game_window[0] + self.game_window[2],
                                                             self.HEIGHT], 0)
            self.field_humidity_slider.draw(screen)
            self.field_radioactivity_slider.draw(screen)
            self.cell_humidity_slider.draw(screen)
            self.cell_radioactivity_slider.draw(screen)

            print_text(screen, self.field_text, self.text_color, self.game_window[0] + self.game_window[2] + 100, 50, 18)
            print_text(screen, self.cell_text, self.text_color, self.game_window[0] + self.game_window[2] + 100, 350, 18)
        else:
            self.game_window[2] = self.game_window_width

    def update(self):
        """changes values of all sliders in settings"""
        self.field_humidity_slider.change_value()
        self.cell.humidity = self.field_humidity_slider.get_value()

        self.field_radioactivity_slider.change_value()
        self.cell.radioactivity = self.field_radioactivity_slider.get_value()

        self.cell_humidity_slider.change_value()
        self.cell.genes[0] = self.cell_humidity_slider.get_value()

        self.cell_radioactivity_slider.change_value()
        self.cell.genes[1] = self.cell_radioactivity_slider.get_value()

        self.cell.change_colors()

    def update_cell(self):
        self.field_humidity_slider.current_value_points = (self.cell.humidity + self.field_humidity_slider.minus_value)\
                                                          * self.field_humidity_slider.scale

        # return round(self.current_value_points / (self.bg_rect[2] / self.upper_value) - self.minus_value)
        self.field_radioactivity_slider.current_value_points = (self.cell.radioactivity + self.field_radioactivity_slider.minus_value) \
                                                          * self.field_radioactivity_slider.scale
        self.cell_humidity_slider.current_value_points = (self.cell.genes[0] + self.cell_humidity_slider.minus_value) \
                                                          * self.cell_humidity_slider.scale
        self.cell_radioactivity_slider.current_value_points = (self.cell.genes[1] + self.cell_radioactivity_slider.minus_value) \
                                                          * self.cell_radioactivity_slider.scale






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
        cloud = self.cloud = 0
        
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
        
        
        #cloud generation
        self.cloud = Cloud(17, 17)
        self.cloud.cells = midpoint_displacement(self.cloud.size_x, 100, -100, 500)
        for i in range(self.cloud.size_x):
            for j in range(self.cloud.size_y):
                if self.cloud.cells[i][j] > 0:
                    self.cloud.cells[i][j] = min(self.cloud.cells[i][j], 100)
                else:
                    self.cloud.cells[i][j] = max(self.cloud.cells[i][j], -100)        
        
        
        def generate_field(cells:list, x, y):
            """generates field initial conditions"""
            for i in range(x):
                for l in range(y):
                    cells[i][l] = Cell()
                    cells[i][l].new_cell(i, l)
                    cells[i][l].radioactivity = -90
                    cells[i][l].food = 30
                    if randint(0, 2):
                        cells[i][l].live = 5
                        cells[i][l].genes[0] = 0
                        cells[i][l].genes[1] = 50
                        #cells[i][l].food = randint(0, 1)
            #generate humadity
            massive = midpoint_displacement(x, 100, -100, 200)
            for i in range(x):
                for j in range(y):
                    if massive[i][j] > 0:
                        self.cells[i][j].humidity = min(massive[i][j], 100)
                    else:
                        self.cells[i][j].humidity = max(massive[i][j], -100)
            #generate radioactivity           
            massive = midpoint_displacement(x, 0, -100, 200)
          #  for i in range(x):
          #      for j in range(y):
          #          if massive[i][j] > 0:
          #              self.cells[i][j].radioactivity = min(massive[i][j], 100)
          #          else:
          #              self.cells[i][j].radioactivity = max(massive[i][j], -100)
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
