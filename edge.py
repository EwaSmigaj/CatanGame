from board import *
import pygame
from math import sqrt

color = {
    -1: (255, 255, 255),
    0: (255, 0, 0),
    1: (0, 255, 0),
    2: (0, 0, 255),
    3: (255, 255, 0),
    4: (245, 158, 255)
}

class Edge:
    def __init__(self, start, end, pos_1, pos_2, width=5):
        self.vertices = (start, end)
        self.pos_1 = pos_1
        self.pos_2 = pos_2
        self.display_pos = []
        self.len = 15
        self.available = True
        self.color = -1
        self.clicked = False
        self.a = width
        self.pos_type = None

    def display(self, screen):
        if self.clicked is True:
            c = color[4]
        else:
            c = color[self.color]
        l = self.len
        a = 5

        #               pos_2
        #               //
        #             //
        #           //
        #         //
        #     pos_1
        if len(self.display_pos) < 4:
            if self.pos_1[0] < self.pos_2[0] and self.pos_1[1] > self.pos_2[1]:
                self.pos_type = 0
                p01 = (self.pos_1[0] + l*sqrt(3)/2, self.pos_1[1] - l/2)
                p02 = (self.pos_2[0] - l*sqrt(3)/2, self.pos_2[1] + l/2)
                self.display_pos.append((p01[0] - a/2, p01[1] - a*sqrt(3)/2))
                self.display_pos.append((p01[0] + a/2, p01[1] + a*sqrt(3)/2))
                self.display_pos.append((p02[0] + a / 2, p02[1] + a * sqrt(3) / 2))
                self.display_pos.append((p02[0] - a / 2, p02[1] - a * sqrt(3) / 2))
                pygame.draw.polygon(screen, c, (self.display_pos[0], self.display_pos[1], self.display_pos[2], self.display_pos[3]))

            # pos_1
            #   \\
            #     \\
            #       \\
            #         \\
            #           pos_2
            elif self.pos_1[0] < self.pos_2[0] and self.pos_1[1] < self.pos_2[1]:
                self.pos_type = 1
                p01 = (self.pos_1[0] + l*sqrt(3)/2, self.pos_1[1] + l/2)
                p02 = (self.pos_2[0] - l*sqrt(3)/2, self.pos_2[1] - l/2)
                self.display_pos.append((p01[0] + a/2, p01[1] - a*sqrt(3)/2))
                self.display_pos.append((p01[0] - a/2, p01[1] + a*sqrt(3)/2))
                self.display_pos.append((p02[0] - a / 2, p02[1] + a * sqrt(3) / 2))
                self.display_pos.append((p02[0] + a / 2, p02[1] - a * sqrt(3) / 2))
                pygame.draw.polygon(screen, c, (self.display_pos[0], self.display_pos[1], self.display_pos[2], self.display_pos[3]))

            #      pos_1
            #       ||
            #       ||
            #       ||
            #       ||
            #      pos_2
            elif self.pos_1[0] == self.pos_2[0]:
                if self.pos_1[1] < self.pos_2[1]:
                    self.pos_type = 2
                    p01 = (self.pos_1[0], self.pos_1[1] + l)
                    p02 = (self.pos_2[0], self.pos_2[1] - l)
                    self.display_pos.append((p01[0] + a, p01[1]))
                    self.display_pos.append((p01[0] - a, p01[1]))
                    self.display_pos.append((p02[0] - a, p02[1]))
                    self.display_pos.append((p02[0] + a, p02[1]))
        pygame.draw.polygon(screen, c, (self.display_pos[0], self.display_pos[1], self.display_pos[2], self.display_pos[3]))

    def is_inside(self, pos):
        if self.pos_type == 0:
            if self.display_pos[0][0] <= pos[0] <= self.display_pos[3][0] and self.display_pos[3][1] <= pos[1] <= self.display_pos[1][1]:
                return True
        elif self.pos_type == 1:
            if self.display_pos[1][0] <= pos[0] <= self.display_pos[3][0] and self.display_pos[0][1] <= pos[1] <= self.display_pos[3][1]:
                return True
        elif self.pos_type == 2:
            if self.display_pos[1][0] <= pos[0] <= self.display_pos[0][0] and self.display_pos[0][1] <= pos[1] <= self.display_pos[2][1]:
                return True
        return False

    def click(self):
        self.clicked = True



