import pygame
from vertex import Vertex
from edge import Edge


class Button:
    def __init__(self, pos, width, height, color, text="", dest=None):
        self.pos = pos
        self.width = width
        self.height = height
        self.color = color
        self.text = text
        self.clicked = False
        self.destination = dest
        self.text_size = {}



    def display(self, screen):
        if self.clicked is True:
            self.color = (123,123,123)
        else:
            self.color = (93,93,93)

        if self.destination is not None:
            multiple_line = self.text.find("\n")
            if multiple_line != -1:
                line_1 = self.text[:multiple_line]
                line_2 = self.text[multiple_line+1:]
            t = self.text if multiple_line == -1 else max(line_1, line_2)

            pygame.draw.rect(screen, self.color, (self.pos[0], self.pos[1], self.width, self.height))

            font_size = self.text_size.get(t, 99)
            text = pygame.font.SysFont(None, font_size)
            text = text.render(t, True, (255, 255, 255))
            text_w = text.get_rect().width

            if text_w >= self.width-10:
                while text_w >= self.width-10:
                    font_size -= 5
                    text = pygame.font.SysFont(None, font_size)
                    text = text.render(t, True, (255, 255, 255))
                    text_w = text.get_rect().width
                self.text_size[t] = font_size
            text_h = text.get_rect().height
            if multiple_line != -1:
                text = pygame.font.SysFont(None, font_size)
                line_1 = text.render(line_1, True, (255, 255, 255))
                line_2 = text.render(line_2, True, (255, 255, 255))
                screen.blit(line_1, (self.pos[0] + (self.width - text_w) / 2, self.pos[1] + (self.height - 2*text_h) / 2))
                screen.blit(line_2, (self.pos[0] + (self.width - line_2.get_rect().width) / 2, self.pos[1] + self.height / 2))
            else:
                screen.blit(text, (self.pos[0]+(self.width - text_w)/2, self.pos[1]+(self.height-text_h)/2))

    def is_inside(self, pos):
        if self.destination is not None:
            if self.pos[0] < pos[0] < self.pos[0] + self.width:
                if self.pos[1] < pos[1] < self.pos[1] + self.height:
                    return True
        return False

    def click(self):
        self.clicked = True

    def change_text(self, new_text):
        self.text = new_text







