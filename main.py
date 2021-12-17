import pygame
from vis import draw_game, draw_menu
from model import *
from objects import *
from controller import *
from numpy import array
BLACK = (0, 0, 0)
# Game screen Height and Width
HEIGHT = 800
WIDTH = 1000

# window with game, rectangle(left up angle coors, width, height)
game_window = array([0, 0, 800, 700])
FPS = 30
# default middle field size
field_size = 150


def menu(field_size):
    """loop for menu, draws menu screen and reads events from user"""
    global Main_menu, Main, Game, screen
    field = Field()
    main_menu = Menu(WIDTH, HEIGHT, game_window)
    clock = pygame.time.Clock()
    pressed_mouse = False
    while Main_menu:
        clock.tick(FPS)
        draw_menu(main_menu, screen)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Main_menu = False
            else:
                Main_menu, pressed_mouse, field_size, field = menu_event_manage(event, field, main_menu, pressed_mouse, Main_menu, field_size)
    return field_size, field




def game(field_size, field):
    """loop for the game, draws game interface and reads events from user"""
    global Game, Main, screen
    # creating initial field
    # field = Field()
    # field.new_field(field_size, field_size)
    clock = pygame.time.Clock()
    # creating interface
    interface = Interface(WIDTH, HEIGHT, game_window)
    settings = Settings(200, HEIGHT, game_window, WIDTH, 0)
    # Constant that shows if mouse button is pressed
    pressed_mouse = False
    # game speed
    speed = 1
    # counter of loops in the game
    loop_counter = 0

    while Game:
        clock.tick(FPS)

        loop_counter += 1
        screen.fill(BLACK)
        # drawing game screen
        draw_game(screen, field, interface, settings)
        pygame.display.update()
        # event processing
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Game = False
            else:
                field, pressed_mouse, interface, speed = \
                    event_manage(event, field, pressed_mouse, interface, speed, settings)

        if get_steps(loop_counter, speed):
            k = time.perf_counter()
            field = step(field)
            print('entire time', time.perf_counter() - k)


def main():
    """main function of the game, everything starts here"""
    global Main, Game, screen, Main_menu, field_size
    pygame.init()
    Main = True
    Game = False
    Main_menu = False
    # main cycle of the game, ends when player exits the game,
    # consists of 2-3 cycles: game menu, game play, game over/game pause !!!Still in discussion about it!!!
    while Main:
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        Main_menu = True
        # loop for menu
        field_size, field = menu(field_size)
        Game = True
        # loop for main game
        game(field_size, field)
        Main = False

    pygame.quit()
    
if __name__ == '__main__':
    main()


