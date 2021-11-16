from random import randint
import pygame
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

    def __init__(self, screen, x, y, color, height, width, text, pushed):
        """x,y - coordinates of left top corner
        color - color of bottom
        text - text on the bottom"""
        self.screen = screen
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.pushed = pushed
        self.color = color
        self.text = text


    def draw(self):
        rect(self.screen, self.color, [self.x, self.y, self.width, self.height])


    class Interface:
        """creates class with all buttons"""

        def __init__(self, pause, play):
            self.game_window = [0, 0, 0, 0]
            self.pause = pause
            self.play = play




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
