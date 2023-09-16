import json

from resources.colors import get_color
from src.entity.ant import Ant
from src.entity.wall import Wall


def read_initial_config():
    with open('config/config.json', 'r') as json_file:
        data = json.load(json_file)
    return data


def read_ants_config(grid_size) -> [Ant]:
    with open('config/scenario.json', 'r') as json_file:
        data = json.load(json_file)

    ants = []
    for i, a in enumerate(data["ant"]):
        ant = Ant(grid_size, a[str(i)]["initial_position"]["row"], a[str(i)]["initial_position"]["col"],
                  a[str(i)]["instructions"], get_color(a[str(i)]["color"]))
        ants.append(ant)
    return ants


def read_walls_config() -> [Wall]:
    with open('config/scenario.json', 'r') as json_file:
        data = json.load(json_file)

    walls = []
    for _, w in enumerate(data["wall"]):
        wall = Wall(w["row"], w["col"])
        walls.append(wall)
    return walls
