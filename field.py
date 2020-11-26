from board import *
import pygame
from math import cos, pi, sin
"""
9 - desert
0 - rock
1 - clay
2 - wood
3 - sheep
4 - hay
"""

pygame.font.init()
types = [0, 1, 2, 3, 4, 9]
color = {
    9: (222,199, 135),
    0: (145, 146, 129),
    1: (245, 145, 69),
    2: (8, 138, 8),
    3: (171, 255, 61),
    4: (230, 203, 0)
}

class Field:
    def __init__(self, tag, type, numb):
        self.tag = tag
        self.type = type
        self.number = numb

    def display(self, screen, position):
        center_x = int(position[1][0])
        center_y = int(position[1][1] + (position[4][1] - position[1][1])/2)
        pygame.draw.polygon(screen, color[self.type], position)
        if self.type != 9:
            c = (0, 0, 0)
            if self.number == 8 or self.number == 6:
                c = (200, 0, 0)
            pygame.draw.circle(screen, (255, 255, 255), (center_x, center_y), 25)
            text = pygame.font.SysFont(None, 40)
            numb = text.render(str(self.number), True, c)
            screen.blit(numb, (center_x-10, center_y-10))
