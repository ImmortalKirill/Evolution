from model import change_scale
import pygame


def zoom(event: pygame.MOUSEBUTTONDOWN, field):
    """checks if event is wheel rolling and changes scale of field(zoom in or out)"""
    # if mouse wheel is rolled forward, zoom in
    if event.button == 4:
        change_scale(field, 1)
    #  if mouse wheel is rolled backward, zoom out
    if event.button == 5:
        change_scale(field, -1)


def mouse_pos_check(mouse_pos, rect):
    """checks if mouse is on rect(left up angle, width, height)"""
    if abs(mouse_pos[0] - (rect[0])) <= rect[2] / 2 and abs(mouse_pos[1] - (rect[1])) <= rect[3] / 2:
        return True
    else:
        return False


def event_manage(event, field, pressed_mouse, game_window):
    """manages event from the game, changes field etc"""
    if event.type == pygame.MOUSEBUTTONDOWN:
        if mouse_pos_check(pygame.mouse.get_pos(), game_window):  # if mouse on game window
            # if pressed button is left mouse button
            if event.button == 1:
                pressed_mouse = True
            # checking if we need to zoom map
            zoom(event, field)
        else:  # managing interface, not now
            pass
    elif event.type == pygame.MOUSEBUTTONUP:
        if event.button == 1:
            pressed_mouse = False
    return field, pressed_mouse


if __name__ == "__main__":
    print("This module is not for direct call!")
