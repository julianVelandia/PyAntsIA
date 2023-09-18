import json

from resources.colors import get_color
from src.entity.ant import Ant
from src.entity.wall import Wall

def read_code_rules():
    with open('config/code_rules.json', 'r') as f:
        rules_dict = json.load(f)
    return rules_dict

def read_initial_config(config_file):
    with open(config_file, 'r') as json_file:
        data = json.load(json_file)
    return data


def read_ants_config(scenario_file, grid_size) -> [Ant]:
    with open(scenario_file, 'r') as json_file:
        data = json.load(json_file)
    ants = []
    for i, a in enumerate(data["ant"]):
        print("holaaaaaa")
        ant = Ant(grid_size, a[str(i)]["initial_position"]["row"], a[str(i)]["initial_position"]["col"],
                  a[str(i)]["instructions"], get_color(a[str(i)]["color"]))
        ants.append(ant)
    return ants


def read_walls_config(config_file) -> [Wall]:
    with open(config_file, 'r') as json_file:
        data = json.load(json_file)

    walls = []
    for _, w in enumerate(data["wall"]):
        wall = Wall(w["row"], w["col"])
        walls.append(wall)
    return walls
