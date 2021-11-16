from model import change_scale, mouse_pos_check
import pygame


def zoom(event: pygame.MOUSEBUTTONDOWN, field):
    """checks if event is wheel rolling and changes scale of field(zoom in or out)"""
    # if mouse wheel is rolled forward, zoom in
    if event.button == 4:
        change_scale(field, 1)
    #  if mouse wheel is rolled backward, zoom out
    if event.button == 5:
        change_scale(field, -1)





def event_manage(event, field, pressed_mouse, interface):
    """manages event from the game, changes field etc"""
    if event.type == pygame.MOUSEBUTTONDOWN:
        if mouse_pos_check(pygame.mouse.get_pos(), interface.game_window):  # if mouse on game window
            # if pressed button is left mouse button
            if event.button == 1:
                pressed_mouse = True
            # checking if we need to zoom map
            zoom(event, field)
        else:  # FixMe managing interface, haven't done
            pass
    elif event.type == pygame.MOUSEBUTTONUP:
        if event.button == 1:
            pressed_mouse = False
    elif event.type == pygame.MOUSEMOTION:  # changing field coors
        if pressed_mouse and mouse_pos_check(pygame.mouse.get_pos(), interface.game_window):
            # moving the map
            field.change_cors([event.rel[i]*0.1*(-1)**(i+1) for i in (0, 1)])

    return field, pressed_mouse, interface


if __name__ == "__main__":
    print("This module is not for direct call!")
