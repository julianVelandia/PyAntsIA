import pygame
import pygame.font
from tkinter import simpledialog
from src.entity.wall import Wall

play_button = []


def create_buttons(global_i, delay, current_step, window_width, window_height, screen, ants, change_code_text,
                   text_code,
                   text_index, increase_velocity, reduce_velocity, restart_simulation, end_simulation):
    font = pygame.font.Font(None, 30)
    small_font = pygame.font.Font(None, 20)

    iteration_text(global_i, font, window_width - window_height // 4, window_height, screen)

    speed_text(delay, font, window_width - window_height // 4, window_height, screen)

    create_button(screen, font, "+", window_width - window_height // 4, window_height // 6 + 40, 50, 50,
                  increase_velocity)

    create_button(screen, font, "-", window_width - window_height // 4 - 55, window_height // 6 + 40, 50, 50,
                  reduce_velocity)

    code_by_ant_text(font, current_step, window_width - window_height // 4, window_height, screen, ants,
                     change_code_text, text_code, text_index,
                     small_font)

    # TODO fix double button tap
    # create_button(screen, font, "Restart", window_width - window_height // 4, window_height - 120, 200, 50, restart_simulation)

    create_button(screen, font, "End", window_width - window_height // 4, window_height - 60, 200, 50,
                  end_simulation)


def code_by_ant_text(font, step, window_width, window_height, screen, ants, change_code_text, text_code, text_index,
                     small_font):
    text = font.render('Agents Code', True, (0, 0, 0))
    text_rect = text.get_rect()
    text_rect.center = (window_width - text_rect.width // 2, window_height // 3)
    screen.blit(text, text_rect)
    for i in range(len(ants)):
        create_button(screen, font, str(i), window_width + (i + 1) * 40, window_height // 3 + 40, 35, 35,
                      change_code_text, str(i))

    move = 0
    for i, text in enumerate(text_code[int(text_index)]):
        if step == i:
            text = '>  ' + text
        text = small_font.render(text, True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.topleft = (window_width - 200, window_height // 2 + move)
        screen.blit(text, text_rect)
        move += 40


def speed_text(delay, font, window_width, window_height, screen):
    text = font.render(f"Speed {round(100 - (100 * (delay / 5000)))}", True, (0, 0, 0))
    text_rect = text.get_rect()
    text_rect.center = (window_width - text_rect.width // 2, window_height // 7)
    screen.blit(text, text_rect)


def iteration_text(global_i, font, window_width, window_height, screen):
    text = font.render(f"Iteration: {global_i}", True, (0, 0, 0))
    text_rect = text.get_rect()
    text_rect.center = (window_width - text_rect.width // 2, window_height // 9)
    screen.blit(text, text_rect)


def create_button(screen, font, text, x, y, width, height, click_event, text_arg=''):
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
