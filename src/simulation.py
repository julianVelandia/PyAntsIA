import math

import pygame
import time
import pygame.font
import threading

from resources.code.translator import translate_instructions
from src.entity.ant import draw_grid, draw_ant, draw_ant_direction, Ant
from resources.code.strategy import strategy_if, strategy_while, strategy_for
from src.entity.wall import draw_wall
from src.gui import create_buttons
from resources.json import read_walls_config, read_ants_config

simulation_running = False
paused = False
delay = 1600
global_i = 0
text_code = []
text_index = 0
red_text = "\033[91m"
reset_color = "\033[0m"
iteration_i = 0


def define_initial_code(ants: [Ant], translate_code):
    global text_code
    inst = []
    for ant in ants:
        if translate_code:
            inst.append(ant.instructions)
            ant.instructions = translate_instructions(ant.instructions)
            if ant.instructions[0] == 'ERROR':
                print(f"{red_text}{ant.instructions[1]}{reset_color}")
                return 'ERROR'
            continue
        inst.append(ant.instructions)
    text_code = inst


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


def start_simulation_thread(
        scenario_file,
        grid_size,
        is_draw_grid,
        screen_size,
        translate_code,
):
    global global_i, iteration_i, simulation_running, paused
    simulation_running = True
    is_in_code_block = False

    pygame.init()

    if screen_size == "full":
        screen_info = pygame.display.Info()
        window_width = screen_info.current_w
        window_height = screen_info.current_h
        screen_size = window_height
    else:
        window_height = screen_size
        window_width = 2 * window_height

    ants = read_ants_config(scenario_file, grid_size)
    walls = read_walls_config(scenario_file)
    err = define_initial_code(ants, translate_code)
    if err == 'ERROR':
        return

    screen = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Py-Ants-IA")


    while simulation_running:
        for ant in ants:
            if ant.instruction_index < len(ant.instructions):
                instruction = ant.instructions[ant.instruction_index]

                if instruction.startswith("for "):
                    ant.instructions, len_sub_instructions = strategy_for(ant.instructions, global_i, ant, walls)
                    instruction = ant.instructions[global_i]

                    if not is_in_code_block:
                        iteration_i +=1
                        iteration_i +=len_sub_instructions
                    is_in_code_block = True
                    iteration_i -= len_sub_instructions
                    print("aaaaaaaa", len_sub_instructions)
                    if len_sub_instructions == 0:
                        is_in_code_block = False
                        iteration_i += len_sub_instructions

                if instruction.startswith("if "):
                    ant.instructions = strategy_if(ant.instructions, global_i, ant, walls)
                    continue

                if instruction.startswith("while "):
                    ant.instructions = strategy_while(ant.instructions, global_i, ant, walls)
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
        print(iteration_i)
        create_buttons(
            global_i, delay, iteration_i, window_width, window_height, screen, ants,
            change_code_text, text_code, text_index, increase_velocity, reduce_velocity)

        # boton de stop con un stop aquí
        pygame.display.flip()
        time.sleep(delay / 5000)
        global_i += 1
        iteration_i += 1



def start_simulation(
        scenario_file='config/scenario.json',
        grid_size=40,
        is_draw_grid=True,
        screen_size="full",
        translate_code=True,
):
    simulation_thread = threading.Thread(target=start_simulation_thread, args=(
        scenario_file,
        grid_size,
        is_draw_grid,
        screen_size,
        translate_code,
    ))
    simulation_thread.start()
