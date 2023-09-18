import math

import pygame
import time
import pygame.font
import threading

from resources.code.translator import translate_instructions
from src.entity.ant import draw_grid, draw_ant, draw_ant_direction
from resources.code.strategy import strategy_if, strategy_while, strategy_for
from src.entity.wall import draw_wall
from src.gui import create_button, iteration_text, speed_text, code_by_ant_text, create_buttons
from resources.json import read_initial_config, read_walls_config, read_ants_config

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


def start_simulation_thread(config_file, scenario_file):
    global global_i, simulation_running, paused
    simulation_running = True

    data = read_initial_config(config_file)
    grid_size = data["grid_size"]
    is_draw_grid = data["is_draw_grid"]
    screen_size = data["screen_size"]
    translate_code = data["translate_code"]

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

    screen = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Py-Ants-IA")

    font = pygame.font.Font(None, 30)
    small_font = pygame.font.Font(None, 20)
    inst = []
    print(len(ants))
    for ant in ants:
        if translate_code:
            print(ant.instructions)
            ant.instructions = translate_instructions(ant.instructions)
            if ant.instructions[0] == 'ERROR':
                red_text = "\033[91m"
                reset_color = "\033[0m"
                print(f"{red_text}{ant.instructions[1]}{reset_color}")
                return

        inst.append(ant.instructions)

    define_initial_code(inst)

    while simulation_running:
        for ant in ants:
            if ant.instruction_index < len(ant.instructions):
                instruction = ant.instructions[ant.instruction_index]

                if instruction.startswith("if "):
                    ant.instructions = strategy_if(ant.instructions, global_i, ant, walls)
                    continue

                if instruction.startswith("while "):
                    ant.instructions = strategy_while(ant.instructions, global_i, ant, walls)
                    instruction = ant.instructions[global_i]

                if instruction.startswith("for "):
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

        create_buttons(global_i, delay, font,window_width,window_height,screen,ants,change_code_text,text_code, text_index, small_font,increase_velocity,reduce_velocity)

        pygame.display.flip()
        time.sleep(delay / 5000)
        global_i += 1




def start_simulation(scenario_file='config/scenario.json', config_file='config/config.json'):
    simulation_thread = threading.Thread(target=start_simulation_thread, args=(config_file, scenario_file))
    simulation_thread.start()
