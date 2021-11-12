import pygame
from vis import *
from model import *
from objects import *
from controller import *

# Game screen Height and Width
HEIGHT = 800
WIDTH = 800

FPS = 30
def main():
    """main function of the game, everything starts here"""
    pygame.init()
    Main = True
    # main cycle of the game, ends when player exits the game,
    # consists of 2-3 cycles: game menu, game play, game over/game pause !!!Still in discussion about it!!!
    while Main:
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        clock = pygame.time.Clock()
        Menu = True
        # loop for menu
        while Menu:  # FixMe
            clock.tick(FPS)
            Menu = False
            Game = True
        # loop for main game
        while Game:  # Fixme
            Game = False
        Main = False
    pygame.quit()


