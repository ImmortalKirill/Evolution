from model import change_scale, mouse_pos_check, find_cell, change_coords
import pygame
from numpy import array


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
        if mouse_pos_check(array(event.pos), interface.game_window):  # if mouse on game window
            # if pressed button is left mouse button
            if event.button == 1:
                pressed_mouse = True
            # checking if we need to zoom map
            zoom(event, field)
            # if mode is cell_spawn

        if interface.cell_spawn.pressed and (not settings.pen.pressed) and (event.button == 3):
            x_cell, y_cell = find_cell(event.pos, field, interface.game_window)
            settings.cell = field.cells[x_cell][y_cell]
            settings.update_slider()


        else:
            # if pressed button is left mouse button
            if event.button == 1:
                pressed_mouse = True
            # if mouse on button pause
            if mouse_pos_check(array(pygame.mouse.get_pos()), interface.pause.bg_rect):
                interface.pause.change_press()
                speed = -speed
            # if mouse on button spawn new cells
            if mouse_pos_check(array(pygame.mouse.get_pos()), interface.cell_spawn.bg_rect):
                interface.cell_spawn.change_press()
                settings.status += 1
            # if mouse on button pen
            if mouse_pos_check(pygame.mouse.get_pos(), settings.pen.bg_rect):
                settings.pen.change_press()
                settings.cell_button.pressed = 1
                settings.field_button.pressed = 1
            if mouse_pos_check(pygame.mouse.get_pos(), settings.cell_button.bg_rect):
                settings.cell_button.change_press()
            if mouse_pos_check(pygame.mouse.get_pos(), settings.field_button.bg_rect):
                settings.field_button.change_press()
            # if mouse on button clear field
            if mouse_pos_check(array(pygame.mouse.get_pos()), interface.clear.bg_rect):
                for i in range(field.size_x):
                    for j in range(field.size_y):
                        field.cells[i][j].live = 0
            # if mouse on button create new field with new population
            if mouse_pos_check(array(pygame.mouse.get_pos()), interface.population_spawn.bg_rect):
                field.new_field(field.size_x, field.size_y)


    elif event.type == pygame.MOUSEBUTTONUP:
        if event.button == 1:
            pressed_mouse = False
    elif event.type == pygame.MOUSEMOTION:  # changing field coors
        if pressed_mouse and mouse_pos_check(array(pygame.mouse.get_pos()), interface.game_window):
            # moving the map
            field.change_cors([event.rel[i] * 0.1 * (-1) ** (i + 1) for i in (0, 1)])

    # drawing pen square
    if (event.type == pygame.MOUSEBUTTONDOWN) or (event.type == pygame.MOUSEMOTION):
        if settings.pen.pressed and pygame.mouse.get_pressed()[2] and mouse_pos_check(array(pygame.mouse.get_pos()),
                                                                                      interface.game_window):
            # finds a square of cells which we change
            x_cell, y_cell = find_cell(event.pos, field, settings.game_window)
            if (x_cell is not None) and (y_cell is not None):  # if cell is in field
                x, y = change_coords([x_cell, y_cell], field.scale, field.x_center, field.y_center,
                                     settings.game_window, 1)
                r = settings.pen_radius.get_value() * field.scale  # radius of pen - 1/2 of square side in cells
                settings.pen_rect = (x - r, y - r, 2 * r, 2 * r)
                for i in range(-settings.pen_radius.get_value(), settings.pen_radius.get_value()):
                    for j in range(-settings.pen_radius.get_value() + 1, settings.pen_radius.get_value() + 1):
                        if (x_cell + i < field.size_x) and (x_cell + i >= 0) and (y_cell + j < field.size_y) and \
                                (y_cell + j >= 0):
                            settings.cell = field.cells[x_cell + i][y_cell + j]
                            settings.redraw()
                            if settings.cell_button.pressed:
                                if x_cell is not None:
                                    field.cells[x_cell + i][y_cell + j].live = 5

    # if mouse on speed_slider
    if pygame.mouse.get_pressed()[0]:
        interface.slider.change_value()
        if not interface.pause.pressed:
            speed = interface.slider.get_value()
        settings.update()

    return field, pressed_mouse, interface, speed


def menu_event_manage(event, main_menu, pressed_mouse, Main_menu, field_size):
    """manages event from the game, changes field etc"""
    if event.type == pygame.MOUSEBUTTONDOWN:
        if mouse_pos_check(array(pygame.mouse.get_pos()), main_menu.start.bg_rect):
            main_menu.start.change_press()
            Main_menu = False
        if mouse_pos_check(array(pygame.mouse.get_pos()), main_menu.small_field.bg_rect):
            main_menu.small_field.change_press()
            field_size = 100
            main_menu.large_field.pressed = 0
            main_menu.middle_field.pressed = 0
        if mouse_pos_check(array(pygame.mouse.get_pos()), main_menu.middle_field.bg_rect):
            main_menu.middle_field.change_press()
            field_size = 150
            main_menu.large_field.pressed = 0
            main_menu.small_field.pressed = 0
        if mouse_pos_check(array(pygame.mouse.get_pos()), main_menu.large_field.bg_rect):
            main_menu.large_field.change_press()
            field_size = 200
            main_menu.small_field.pressed = 0
            main_menu.middle_field.pressed = 0

    return Main_menu, pressed_mouse, field_size


if __name__ == "__main__":
    print("This module is not for direct call!")
