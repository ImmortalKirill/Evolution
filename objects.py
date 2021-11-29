from random import randint
import pygame
import pygame.freetype
from pygame.draw import *


class Cell():
    """ class of one cell on a Field"""

    def __init__(self):
        live = self.live = 0
        x = self.x = 0
        y = self.y = 0
        self.color = (255, 255, 255)
        self.color_bg = (0, 0, 0)
        max_live = self.max_live = 1
        self.genes = [0, 0]
        self.humidity = 0
        # radioactive resistance
        self.radioactivity = 0

    def new_cell(self, x0, y0):
        x = self.x = x0
        y = self.y = y0
    def change_colors(self):
        """changes color of cell and cell_bg according to genes"""
        self.color = (round(255*(self.genes[1] + 100)/200), 0, round(255*(self.genes[0] + 100)/200))
        self.color_bg = (round(255*(self.radioactivity + 100)/200),
                         0,
                         round(255*(self.humidity + 100)/200))
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
                 upper_value: int = 10, current_value_points: int = 30):
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

    # returns the current value of the slider
    def get_value(self) -> float:
        return round(self.current_value_points / (self.bg_rect[2] / self.upper_value))

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
            if pygame.mouse.get_pressed()[0]:
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
        for i in range(x):
            for l in range(y):
                self.cells[i][l] = Cell()
                self.cells[i][l].new_cell(i, l)
                if randint(0, 2):
                    self.cells[i][l].live = 1
        self.cells[5][5].live = 1
        self.cells[5][4].live = 1
        self.cells[5][3].live = 1
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
