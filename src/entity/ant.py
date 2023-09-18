import pygame

from resources.colors import get_color


class Ant:
    def __init__(self, grid_size, row, col, instructions: [str], color):
        self.grid_size = grid_size
        self.grid = [[0] * grid_size for _ in range(grid_size)]
        self.row = row
        self.col = col
        self.direction = "up"
        self.instructions = instructions
        self.instruction_index = 0
        self.color = color

    def move(self, walls):
        if not self.is_wall_in_front(walls):
            if self.direction == "up":
                self.row -= 1
            elif self.direction == "down":
                self.row += 1
            elif self.direction == "left":
                self.col -= 1
            elif self.direction == "right":
                self.col += 1

        self.row = (self.row + self.grid_size) % self.grid_size
        self.col = (self.col + self.grid_size) % self.grid_size

    def turn_right(self):
        if self.direction == "up":
            self.direction = "right"
        elif self.direction == "right":
            self.direction = "down"
        elif self.direction == "down":
            self.direction = "left"
        elif self.direction == "left":
            self.direction = "up"

    def turn_left(self):
        if self.direction == "up":
            self.direction = "left"
        elif self.direction == "left":
            self.direction = "down"
        elif self.direction == "down":
            self.direction = "right"
        elif self.direction == "right":
            self.direction = "up"

    def toggle_cell(self):
        self.grid[self.row][self.col] ^= 1

    def is_wall_in_front(self, walls):
        if self.direction == "up":
            return any(wall.row == self.row - 1 and wall.col == self.col for wall in walls)
        elif self.direction == "down":
            return any(wall.row == self.row + 1 and wall.col == self.col for wall in walls)
        elif self.direction == "left":
            return any(wall.row == self.row and wall.col == self.col - 1 for wall in walls)
        elif self.direction == "right":
            return any(wall.row == self.row and wall.col == self.col + 1 for wall in walls)

    def is_wall_on_right(self, walls):
        if self.direction == "up":
            return any(wall.row == self.row and wall.col == self.col + 1 for wall in walls)
        elif self.direction == "down":
            return any(wall.row == self.row and wall.col == self.col - 1 for wall in walls)
        elif self.direction == "left":
            return any(wall.row == self.row + 1 and wall.col == self.col for wall in walls)
        elif self.direction == "right":
            return any(wall.row == self.row - 1 and wall.col == self.col for wall in walls)

    def is_wall_on_left(self, walls):
        if self.direction == "up":
            return any(wall.row == self.row and wall.col == self.col - 1 for wall in walls)
        elif self.direction == "down":
            return any(wall.row == self.row and wall.col == self.col + 1 for wall in walls)
        elif self.direction == "left":
            return any(wall.row == self.row - 1 and wall.col == self.col for wall in walls)
        elif self.direction == "right":
            return any(wall.row == self.row + 1 and wall.col == self.col for wall in walls)

    def change_color(self, color):
        self.color = get_color(color)

    def is_ant_in_front(self, ants):
        if self.direction == "up":
            return any(ant.row == self.row - 1 and ant.col == self.col for ant in ants)
        elif self.direction == "down":
            return any(ant.row == self.row + 1 and ant.col == self.col for ant in ants)
        elif self.direction == "left":
            return any(ant.row == self.row and ant.col == self.col - 1 for ant in ants)
        elif self.direction == "right":
            return any(ant.row == self.row and ant.col == self.col + 1 for ant in ants)

    def get_ant_in_front_instructions(self, ants):
        if self.is_ant_in_front(ants):
            for ant in ants:
                if self.direction == "up" and ant.row == self.row - 1 and ant.col == self.col:
                    return ant.instructions
                elif self.direction == "down" and ant.row == self.row + 1 and ant.col == self.col:
                    return ant.instructions
                elif self.direction == "left" and ant.row == self.row and ant.col == self.col - 1:
                    return ant.instructions
                elif self.direction == "right" and ant.row == self.row and ant.col == self.col + 1:
                    return ant.instructions
        return []

def draw_ant(screen, ant, cell_size):
    ant_size = cell_size
    pygame.draw.rect(screen, ant.color, (ant.col * cell_size, ant.row * cell_size, ant_size, ant_size))


def draw_ant_direction(screen, ant, cell_size):
    line_length = cell_size // 2
    ant_center_x = ant.col * cell_size + cell_size // 2
    ant_center_y = ant.row * cell_size + cell_size // 2

    if ant.direction == "up":
        pygame.draw.line(screen, (0, 0, 0), (ant_center_x, ant_center_y), (ant_center_x, ant_center_y - line_length),
                         2)
    elif ant.direction == "down":
        pygame.draw.line(screen, (0, 0, 0), (ant_center_x, ant_center_y), (ant_center_x, ant_center_y + line_length),
                         2)
    elif ant.direction == "left":
        pygame.draw.line(screen, (0, 0, 0), (ant_center_x, ant_center_y), (ant_center_x - line_length, ant_center_y),
                         2)
    elif ant.direction == "right":
        pygame.draw.line(screen, (0, 0, 0), (ant_center_x, ant_center_y), (ant_center_x + line_length, ant_center_y),
                         2)


def draw_grid(screen, cell_size):
    for x in range(0, screen.get_height(), cell_size):
        pygame.draw.line(screen, (200, 200, 200), (x, 0), (x, screen.get_height()))
        pygame.draw.line(screen, (200, 200, 200), (0, x), (screen.get_height(), x))
