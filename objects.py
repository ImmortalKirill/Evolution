from random import randint
import pygame
import pygame.freetype
import math
from pygame.draw import *


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


from model import mouse_pos_check


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

    # returns the current value of the slider
    def get_value(self) -> float:
        return round(self.current_value_points / (self.bg_rect[2] / self.upper_value) - self.minus_value)

    # renders slider and the text showing the value of the slider
    def draw(self, display: pygame.display) -> None:
        # draw outline and slider rectangles
        pygame.draw.rect(display, self.bg_color, (self.bg_rect[0], self.bg_rect[1],
                                                  self.bg_rect[2], self.bg_rect[3]), 1)

        pygame.draw.rect(display, self.bg_color, (self.bg_rect[0], self.bg_rect[1],
                                                  self.current_value_points, self.bg_rect[3] - 3))

        # determine size of font
        self.font = pygame.font.Font(pygame.font.get_default_font(), int((50 / 100) * self.bg_rect[3]))

        # create text surface with value
        valueSurf = self.font.render(f"{self.text}: {self.get_value()}", True, self.text_color)

        # centre text
        textx = self.bg_rect[0] + (self.bg_rect[2] / 2) - (valueSurf.get_rect().width / 2)
        texty = self.bg_rect[1] + (self.bg_rect[3]) + 3 * (valueSurf.get_rect().height / 2)

        display.blit(valueSurf, (textx, texty))

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


class Menu(Interface):
    """creates class of additional menu with buttons"""

    def __init__(self, game_window, width, height):
        super().__init__(game_window, width, height)
        self.background_color = (100, 100, 100)
        self.field_humidity_slider = Slider(bg_rect=[self.game_window[0] + self.game_window[2] + 10, 100, 150, 30],
                                            text='humidity', upper_value=200, minus_value=100)
        self.field_radioactivity_slider = Slider(bg_rect=[self.game_window[0] + self.game_window[2] + 10, 200, 150, 30],
                                                 text='radioactivity', upper_value=200, minus_value=100)
        self.font = 0
        self.text = 'Field'
        self.text_color = 'black'

    def draw(self, screen):
        pygame.draw.rect(screen, self.background_color, [self.game_window[0] + self.game_window[2], 0,
                                                         self.WIDTH + self.game_window[0] + self.game_window[2],
                                                         self.HEIGHT], 0)
        self.field_humidity_slider.draw(screen)
        self.field_radioactivity_slider.draw(screen)

        self.font = pygame.font.Font(pygame.font.get_default_font(), 18)
        valueSurf = self.font.render(str(self.text), True, self.text_color)
        screen.blit(valueSurf, (self.game_window[0] + self.game_window[2] + 100, 50))


class Field():
    """ class Field, consists of cells"""

    def __init__(self):
        cells = self.cells = [[]]
        x_center = self.x_center = 0
        y_center = self.y_center = 0
        scale = self.scale = 50
        size_x = self.size_x = 0
        size_y = self.size_y = 0

    def new_field(self, x, y):
        """ creates new field with size x:y cells"""
        self.cells = [[0] * y for l in range(x)]
        def generate_field(cells:list, x, y):
            """generates field initial conditions"""
            for i in range(x):
                for l in range(y):
                    cells[i][l] = Cell()
                    cells[i][l].new_cell(i, l)
                    if randint(0, 2):
                        cells[i][l].live = 5
                        cells[i][l].genes[0] = 0
                        cells[i][l].genes[1] = 50
            for i in range(x):
                for l in range(y):
                    cells[i][l].humidity = -90 + (i + l)
                    cells[i][l].radioactivity = 100
                    if cells[i][l].humidity > 100:
                        cells[i][l].humidity = 100
                    elif cells[i][l].humidity < -100:
                        cells[i][l].humidity = -100
                    cells[i][l].food = randint(0, 1)        
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
