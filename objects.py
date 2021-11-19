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
        max_live = self.max_live = 1
        

    def new_cell(self, x0, y0):
        x = self.x = x0
        y = self.y = y0


class Button:
    """class of buttons"""

    def __init__(self, bg_rect: list, text_color, bg_color, text, angle):
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

    def draw(self, screen):
        """draws button with text on the screen"""
        rect(screen, self.bg_color, self.bg_rect)

        font = pygame.freetype.SysFont("Arial", 10)  # FIXME text

        font.render_to(screen, (self.bg_rect[0] + 5, self.bg_rect[1] + 5), self.text, fgcolor=self.text_color,
                       bgcolor=self.bg_color, rotation=self.angle, size=24)

        text_rect_fig = pygame.freetype.Font.get_rect(font, self.text, size=24)

        self.text_rect[0] = text_rect_fig.left
        self.text_rect[1] = text_rect_fig.top
        self.text_rect[2] = text_rect_fig.width
        self.text_rect[3] = text_rect_fig.height
    def change_press(self):
        """changes state of button"""
        self.pressed += 1
        self.pressed = self.pressed % 2
class Bar(Button):
    """class of moving bars, inherits everything from class Button but  also has attribute fillness"""
    pass

class Interface:
    """creates class with all buttons"""

    def __init__(self, width,  height, game_window):
        """WIDTH, HEIGHT - size of the game"""
        self.game_window = game_window
        self.WIDTH = width
        self.HEIGHT = height
        # Buttons of Interface
        # FixME This should be a real button with position
        self.pause = Button([0, 0, 100, 30], (0, 0, 0), (255, 255, 255), 'Pause', 0)
        self.cell_spawn = Button([0, 600, 100, 30], (0, 0, 0), (255, 255, 255), 'Spawn', 0)
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
                        self.WIDTH, self.HEIGHT - self.game_window[1] - self.game_window[3]], 0
                         )
        # right rect
        pygame.draw.rect(screen, self.background_color, [self.game_window[0] + self.game_window[2], 0,
                        self.WIDTH - self.game_window[0] - self.game_window[2], self.HEIGHT], 0
                         )
        # drawing buttons
        self.pause.draw(screen)



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
