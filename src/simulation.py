import math

import pygame
import time
import pygame.font
import threading

from src.entity.ant import Ant, draw_grid, draw_ant, draw_ant_direction
from resources.code.strategy import strategy_if, strategy_while, strategy_for
from src.entity.wall import Wall, draw_wall
from src.gui import create_button
from src.json import read_initial_config, read_walls_config, read_ants_config

simulation_running = False
paused = False
delay = 1600
global_i = 0
text_code = []
text_index = 0

def define_initial_code(instructions: [str]):
    global text_code
    text_code = instructions

def increase_velocity():
    global delay
    if delay != 200:
        delay -= 200

def reduce_velocity():
    global delay
    if delay != 4000:
        delay += 200

def change_code_text(i):
    global text_index
    text_index = i

def start_simulation():
    global global_i, simulation_running, paused
    simulation_running = True

    data = read_initial_config()
    grid_size = data["grid_size"]
    is_draw_grid = data["is_draw_grid"]
    screen_size = data["screen_size"]
    ants = read_ants_config(grid_size)
    walls = read_walls_config()
    window_height = screen_size
    window_width = 2 * window_height

    pygame.init()
    screen = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Py-Ant-IA")

    font = pygame.font.Font(None, 30)
    small_font = pygame.font.Font(None, 20)
    inst = []
    for ant in ants:
        inst.append(ant.instructions)
    define_initial_code(inst)

    while simulation_running:
        for ant in ants:
            if ant.instruction_index < len(ant.instructions):
                instruction = ant.instructions[ant.instruction_index]

                if instruction.startswith("if"):
                    ant.instructions = strategy_if(ant.instructions, global_i, ant, walls)
                    continue

                if instruction.startswith("while"):
                    ant.instructions = strategy_while(ant.instructions, global_i, ant, walls)
                    instruction = ant.instructions[global_i]

                if instruction.startswith("for"):
                    ant.instructions = strategy_for(ant.instructions, global_i, ant, walls)
                    instruction = ant.instructions[global_i]

                exec(instruction)
                ant.instruction_index += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        screen.fill((255, 255, 255))

        cell_size = screen_size // grid_size
        for wall in walls:
            draw_wall(screen, wall, cell_size)

        if is_draw_grid:
            draw_grid(screen, cell_size)

        for ant in ants:
            draw_ant(screen, ant, cell_size)
            draw_ant_direction(screen, ant, cell_size)

        text = font.render(f"Iteración: {global_i}", True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (window_width - text_rect.width // 2, window_height // 9)
        screen.blit(text, text_rect)

        text = font.render(f"Velocidad {round(100-(100 * (delay / 5000)))}", True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (window_width - text_rect.width // 2, window_height // 7)
        screen.blit(text, text_rect)

        create_button(screen, font, "+", window_width - text_rect.width // 2, window_height // 6 + 40, 50, 50,
                      increase_velocity)

        create_button(screen, font, "-", window_width - text_rect.width // 2 - 55, window_height // 6 + 40, 50, 50,
                      reduce_velocity)

        text = font.render('Codigos', True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (window_width - text_rect.width // 2, window_height // 5)
        screen.blit(text, text_rect)
        for i in range(len(ants)):
            create_button(screen, font, str(i), window_width // 3 + (i+1)*40, window_height // 4, 35, 35,
                          change_code_text, i)

        move = 0
        step = global_i-(len(text_code[text_index])*math.floor(global_i/len(text_code[text_index])))
        print("step: " + str(step))
        print("global_i: " + str(global_i))
        print("len(text_code[text_index]): " + str(len(text_code[text_index])))
        print("math.ceil(global_i/len(text_code[text_index])): " + str(math.ceil(global_i/len(text_code[text_index]))))

        for i, text in enumerate(text_code[text_index]):

            if step == i:
                text = '>  ' + text
            text = small_font.render(text, True, (0, 0, 0))
            text_rect = text.get_rect()
            text_rect.topleft = (window_width // 3, window_height // 9 + move)
            screen.blit(text, text_rect)
            move += 40

        pygame.display.flip()
        time.sleep(delay / 5000)
        global_i += 1


def start_simulation_thread():
    global simulation_thread
    simulation_thread = threading.Thread(target=start_simulation)
    simulation_thread.start()
