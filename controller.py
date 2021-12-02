from model import change_scale, mouse_pos_check, find_cell
import pygame


def zoom(event: pygame.MOUSEBUTTONDOWN, field):
    """checks if event is wheel rolling and changes scale of field(zoom in or out)"""
    # if mouse wheel is rolled forward, zoom in
    if event.button == 4:
        change_scale(field, 1)
    #  if mouse wheel is rolled backward, zoom out
    if event.button == 5:
        change_scale(field, -1)


def event_manage(event, field, pressed_mouse, interface, speed, settings):
    """manages event from the game, changes field etc"""
    if event.type == pygame.MOUSEBUTTONDOWN:
        if mouse_pos_check(event.pos, interface.game_window):  # if mouse on game window
            # if pressed button is left mouse button
            if event.button == 1:
                pressed_mouse = True
            # checking if we need to zoom map
            zoom(event, field)
            # if mode is cell_spawn
            if interface.cell_spawn.pressed and event.button == 3:
                x_cell, y_cell = find_cell(event.pos, field, interface.game_window)
                settings.cell = field.cells[x_cell][y_cell]
                settings.update_cell()
                if x_cell != None:
                    field.cells[x_cell][y_cell].live = 5
        else:
            # if pressed button is left mouse button
            if event.button == 1:
                pressed_mouse = True
            # if mouse on button pause
            if mouse_pos_check(pygame.mouse.get_pos(), interface.pause.bg_rect):
                interface.pause.change_press()
                speed = -speed
            # if mouse on button spawn new cells
            if mouse_pos_check(pygame.mouse.get_pos(), interface.cell_spawn.bg_rect):
                interface.cell_spawn.change_press()
                settings.status += 1
            # if mouse on button clear field
            if mouse_pos_check(pygame.mouse.get_pos(), interface.clear.bg_rect):
                for i in range(field.size_x):
                    for j in range(field.size_y):
                        field.cells[i][j].live = 0
            # if mouse on button create new field with new population
            if mouse_pos_check(pygame.mouse.get_pos(), interface.population_spawn.bg_rect):
                field.new_field(field.size_x, field.size_y)

    elif event.type == pygame.MOUSEBUTTONUP:
        if event.button == 1:
            pressed_mouse = False
    elif event.type == pygame.MOUSEMOTION:  # changing field coors
        if pressed_mouse and mouse_pos_check(pygame.mouse.get_pos(), interface.game_window):
            # moving the map
            field.change_cors([event.rel[i] * 0.1 * (-1) ** (i + 1) for i in (0, 1)])
    # if mouse on speed_slider
    if pygame.mouse.get_pressed()[0]:
        interface.slider.change_value()
        if not interface.pause.pressed:
            speed = interface.slider.get_value()
        settings.update()


    return field, pressed_mouse, interface, speed


if __name__ == "__main__":
    print("This module is not for direct call!")
