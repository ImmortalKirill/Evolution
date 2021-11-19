import pygame
from vis import draw_game
from model import *
from objects import *
from controller import *

BLACK = (0,0,0)
# Game screen Height and Width
HEIGHT = 800
WIDTH = 800

# window with game, rectangle(left up angle cors, width, height)
game_window = (50, 50, 500, 500)
FPS = 30
def menu():
    """loop for menu, draws menu screen and reads events from user"""
    pass
def game():
    """loop for the game, draws game interface and reads events from user"""
    global Game, Main, screen
    # creating initial field
    field = Field()
    field.new_field(100, 100)
    clock = pygame.time.Clock()
    # creating interface
    interface = Interface(WIDTH, HEIGHT, game_window)
    # Constant that shows if mouse button is pressed
    pressed_mouse = False
    # game speed
    speed = 1
    # counter of loops if the game
    loop_counter = 0
    while Game:
        clock.tick(FPS)

        loop_counter += 1
        screen.fill(BLACK)
        # drawing game screen
        draw_game(screen, field, interface)
        pygame.display.update()
        # event processing
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Game = False
            else:
                field, pressed_mouse, interface, speed = event_manage(event, field, pressed_mouse, interface, speed)
        for i in range(get_steps(loop_counter, speed)):
            step(field)


def main():
    """main function of the game, everything starts here"""
    global Main, Game, screen
    pygame.init()
    Main = True
    Game = False
    # main cycle of the game, ends when player exits the game,
    # consists of 2-3 cycles: game menu, game play, game over/game pause !!!Still in discussion about it!!!
    while Main:
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        Menu = True
        # loop for menu
        menu()
        Game = True
        # loop for main game
        game()
        Main = False

    pygame.quit()
    
    
main()


