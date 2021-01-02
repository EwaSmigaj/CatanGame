from button import Button
from vertex import Vertex
from edge import Edge
import pygame


class OptionButton(Button):
    def __init__(self, pos, width, height, color, txt_def="build ", dest_def=None):
        super().__init__(pos, width, height, color)

    def set_text(self):
        dest_txt = {
            "village": "build village",
            "town": "build town",
            "road": "build road",
            "development card": "buy development card"
        }
        self.text = dest_txt[self.destination]

    def display(self, screen, init=False):
        if self.destination is not None or init is False:
            if self.destination is None:
                self.destination = "development card"
            self.set_text()
            pygame.draw.rect(screen, (138, 115, 73), (self.pos[0], self.pos[1], self.width, self.height))
            font_size = 100
            txt_w = self.width + 1
            while txt_w > self.width-10:
                text = pygame.font.SysFont(None, font_size)
                txt = text.render(self.text, True, (255, 255, 255))
                txt_w = txt.get_rect().width
                font_size -= 5
            screen.blit(txt, (self.pos[0]+(self.width - txt_w)/2, self.pos[1]+(self.height-txt.get_rect().height)/2))

    def is_inside(self, mouse_coordinates):
        if self.destination is not None:
            if self.pos[0] < mouse_coordinates[0] < self.pos[0] + self.width:
                if self.pos[1] < mouse_coordinates[1] < self.pos[1] + self.height:
                    return True
        return False

    def change_dest(self, dest_instance):
        if dest_instance is None:
            self.destination = None
        elif type(dest_instance) == Vertex:
            if dest_instance.building == 0:
                self.destination = "village"
            if dest_instance.building == 1:
                self.destination = "town"
        elif type(dest_instance) == Edge:
            self.destination = "road"
        else:
            self.destination = dest_instance

    def click(self):
        self.clicked = True



