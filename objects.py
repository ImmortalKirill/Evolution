from random import randint
import pygame
from pygame.draw import *
from pygame import freetype


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

    def __init__(self, screen, bg_rect: list, text_color, bg_color, text, angle, pushed):
        """x,y - coordinates of left top corner
        color - color of bottom
        text - text on the bottom
        bg_rect = list [x, y, width, height] where x,y - coordinates of left top angle of rect of background
        text_rect = list [x, y, width, height] where x,y - coordinates of left top angle of rect of text"""
        self.screen = screen
        # self.x = x
        # self.y = y
        # self.height = height
        # self.width = width
        self.pushed = pushed
        self.text_color = text_color
        self.text = text
        self.bg_color = bg_color
        self.bg_rect = bg_rect
        self.text_rect = [0, 0, 0, 0]
        self.angle = angle

    def draw(self):
        """draws button with text"""
        rect(self.screen, self.bg_color, self.bg_rect)
        font = pygame.freetype.SysFont("Arial", 18)  # FIXME text

        font.render_to(self.screen, (self.bg_rect[0] + 5, self.bg_rect[1] + 5), self.text, fgcolor=self.text_color,
                       bgcolor=self.bg_color, rotation=self.angle, size=24)

        text_rect_fig = pygame.freetype.Font.get_rect(font, self.text, size=24)

        self.text_rect[0] = text_rect_fig.left
        self.text_rect[1] = text_rect_fig.top
        self.text_rect[2] = text_rect_fig.width
        self.text_rect[3] = text_rect_fig.height
        print(self.text_rect)




class Interface:
    """creates class with all buttons"""

    def __init__(self, pause, play):
        self.game_window = [0, 0, 0, 0]
        self.pause = pause
        self.play = play

    def draw(self):
        self.play.draw()
        self.pause.draw()




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
