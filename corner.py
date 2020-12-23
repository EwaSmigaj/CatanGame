# buildings:
# 1 - village
# 2 - town
import pygame
from math import sqrt

color = {
    -1: (255, 255, 255),
    0: (255, 0, 0),
    1: (0, 0, 255),
    2: (0, 255, 0),
    3: (255, 255, 0)
}
image_name = {
    0: "RED",
    1: "GREEN",
    2: "BLUE",
    3: "YELLOW"
}

class Corner:
    def __init__(self, numb, pos_x=0, pos_y=0, c=-1, corner_size=30):
        self.numb = numb
        self.color = c
        self.empty = True
        self.building = 0
        self.available = True
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.corner_size = 30
        self.clicked = False

    def display(self, screen):
        # pass
        if self.clicked is True:
            clicked = "_clicked"
        else:
            clicked = ""

        if self.building == 0:
            filename = "Graphic//corner_empty" + clicked + ".png"
            img = pygame.image.load(filename)
            img = pygame.transform.scale(img, (self.corner_size, self.corner_size))
            screen.blit(img, (self.pos_x - int(self.corner_size/2), self.pos_y - int(self.corner_size/2)))

        elif self.building == 1:
            filename = "Graphic//village_" + image_name[self.color] + clicked + ".png"
            img = pygame.image.load(filename)
            img = pygame.transform.scale(img, (self.corner_size, self.corner_size))
            screen.blit(img, (self.pos_x - int(self.corner_size/2), self.pos_y - int(self.corner_size/2)))

        elif self.building == 2:
            filename = "Graphic//town_" + image_name[self.color] + ".png"
            img = pygame.image.load(filename)
            img = pygame.transform.scale(img, (self.corner_size, self.corner_size))
            screen.blit(img, (self.pos_x - int(self.corner_size/2), self.pos_y - int(self.corner_size/2)))

    def is_inside(self, pos):
        dist = sqrt((self.pos_x - pos[0])**2 + (self.pos_y - pos[1])**2)
        if dist < self.corner_size/2:
            return True
        else:
            return False

    def click(self):
        if self.building != 2:
            self.clicked = True

