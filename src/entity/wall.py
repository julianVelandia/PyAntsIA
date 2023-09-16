import pygame


class Wall:
    def __init__(self, row, col):
        self.row = row
        self.col = col

def draw_wall(screen, wall, cell_size):
    wall_color = (100, 100, 100)
    pygame.draw.rect(screen, wall_color, (wall.col * cell_size, wall.row * cell_size, cell_size, cell_size))
