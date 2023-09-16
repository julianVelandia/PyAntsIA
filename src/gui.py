import pygame
from tkinter import simpledialog

from src.entity.wall import Wall




play_button = []




def create_button(screen, font, text, x, y, width, height, click_event, text_arg = ''):
    button_rect = pygame.Rect(x, y, width, height)

    is_hover = button_rect.collidepoint(pygame.mouse.get_pos())

    if is_hover:
        pygame.draw.rect(screen, (150, 150, 150), button_rect)
    else:
        pygame.draw.rect(screen, (100, 100, 100), button_rect)

    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=button_rect.center)
    screen.blit(text_surface, text_rect)

    if is_hover and pygame.mouse.get_pressed()[0]:
        if text_arg == '':
            click_event()
        else:
            click_event(text_arg)



def pause_simulation():
    global paused
    paused = not paused


def end_simulation():
    global global_i, simulation_running
    global_i = 0
    simulation_running = False

def agregar_pared():
    global walls
    row = simpledialog.askinteger("Agregar Pared", "Fila:")
    col = simpledialog.askinteger("Agregar Pared", "Columna:")

    if row is not None and col is not None:
        walls.append(Wall(row, col))

