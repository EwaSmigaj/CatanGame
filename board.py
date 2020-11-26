from field import *
from corner import *
from edge import *
from button import *
import random
import pygame
from math import sqrt
from optionbutton import *

color = {
    -1: (255, 255, 255),
    0: (255, 0, 0),
    1: (0, 255, 0),
    2: (0, 0, 255),
    3: (255, 255, 0)
}
types_names = ["wood", "clay", "sheep", "hay", "rock"]
dev_cards_names = ["knight", "victory_point"]
numbs = [6, 5, 9, 4, 3, 8, 10, 6, 5, 9, 12, 3, 2, 10, 11, 11, 4, 8]
fields = [9, 0, 0, 0, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4]
random.shuffle(fields)
corners_fields = {
           0: [0, 1, 2, 10, 9, 8],
           1: [2, 3, 4, 12, 11, 10],
           2: [4, 5, 6, 14, 13, 12],
           3: [7, 8, 9, 19, 18, 17],
           4: [9, 10, 11, 21, 20, 19],
           5: [11, 12, 13, 23, 22, 21],
           6: [13, 14, 15, 25, 24, 23],
           7: [16, 17, 18, 29, 28, 27],
           8: [18, 19, 20, 31, 30, 29],
           9: [20, 21, 22, 33, 32, 31],
           10: [22, 23, 24, 35, 34, 33],
           11: [24, 25, 26, 37, 36, 35],
           12: [28, 29, 30, 40, 39, 38],
           13: [30, 31, 32, 42, 41, 40],
           14: [32, 33, 34, 44, 43, 42],
           15: [34, 35, 36, 46, 45, 44],
           16: [39, 40, 41, 49, 48, 47],
           17: [41, 42, 43, 51, 50, 49],
           18: [43, 44, 45, 53, 52, 51]
            }
corners_corners = {
            0: [1, 8],
            1: [0, 2],
            2: [1, 3, 10],
            3: [2, 4],
            4: [3, 5, 12],
            5: [4, 6],
            6: [5, 14],
            7: [8, 17],
            8: [7, 9, 0],
            9: [8, 10, 19],
            10: [9, 11, 2],
            11: [10, 12, 21],
            12: [11, 13, 4],
            13: [12, 14, 23],
            14: [13, 15, 6],
            15: [14, 25],
            16: [17, 27],
            17: [16, 18, 7],
            18: [17, 19, 29],
            19: [18, 20, 9],
            20: [19, 21, 31],
            21: [20, 22, 11],
            22: [21, 23, 33],
            23: [22, 24, 13],
            24: [23, 25, 35],
            25: [24, 26, 15],
            26: [25, 37],
            27: [16, 28],
            28: [27, 29, 38],
            29: [28, 30, 18],
            30: [29, 31, 40],
            31: [30, 32, 20],
            32: [31, 33, 42],
            33: [32, 34, 22],
            34: [33, 35, 44],
            35: [34, 36, 24],
            36: [35, 37, 46],
            37: [36, 26],
            38: [28, 39],
            39: [38, 40, 47],
            40: [39, 41, 30],
            41: [40, 42, 49],
            42: [41, 43, 32],
            43: [42, 44, 51],
            44: [43, 45, 34],
            45: [44, 46, 53],
            46: [45, 36],
            47: [48, 39],
            48: [47, 49],
            49: [48, 50, 41],
            50: [49, 51],
            51: [50, 52, 43],
            52: [51, 53],
            53: [52, 45]
        }
corners_ports = {
    (1, 0): "wood",
    (3, 4): "sheep",
    (14, 15): "rock",
    (37, 26): "hay",
    (45, 46): "clay",
    (50, 51): "wood",
    (48, 47): "sheep",
    (28, 38): "hay",
    (7, 17): "rock",
                 }
corners_pos = []
spots = 54

'''
self.spots - number of corners
self.players - dict of players {1: <player obj>, 2: <player obj>, ...}
self.fields = [] - list of field objects
self.corners = [] - list of corner objects
self.edges = {} - dict of edge object (key: touple of corners which edge connects, val: edge obj)
self.buildings_sports = {} - dict of buildings already builded during the game
e.g. self.building_spots = {
                            <player number>: {
                                                "buildings": [],
                                                "roads": []
                                              }
                            }
self._fields_corners_map - dict with assigned corners numbs to fields numbs
self._corners_corners_map - dict with assigned corners neighbours 
'''


class Board:
    def __init__(self, players_am, screen_w=1200, screen_h=720, corners_ports=corners_ports, fields_map=corners_fields, corners_map=corners_corners, spots=spots):
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.screen = pygame.display.set_mode((screen_w, screen_h))
        self.spots = spots
        self.turn = -1
        self.fields = []
        self.corners = []
        self.edges = {}
        self.buildings_spots = {}
        self.fields_corners_map = fields_map
        self.corners_corners_map = corners_map
        self.corners_ports = corners_ports
        self.message = "what do you want to do?"
        self.pos_start_x = 100
        self.pos_start_y = 100
        self.edge_length = (5/6 * self.screen_h) / 10
        self.last_click = None
        self.main_panel_x = self.pos_start_x + 12*self.edge_length*sqrt(3)/2
        self.change_buttons = []
        self.option_button = OptionButton((self.main_panel_x + (self.screen_w - self.main_panel_x)/2 - 100, 100), 200, 50, (124,134,123))
        self.end_button = Button((self.screen_w - 400, self.screen_h - 150), 150, 50, (124,134,123), "end ture", "end")
        # self.trade_buttons = OptionButton((self.screen_w - 400, self.screen_h - 250), 100, 40, "trade", "trade")
        self.init_players(players_am)
        self.init_fields()
        self.init_corners()
        self.init_edges()

    def init_change_buttons(self, current_player):
        dist_between_buttons = (self.screen_w - self.main_panel_x) / 5
        button_w = dist_between_buttons - 20
        for i, prod in enumerate(current_player.possible_trades):
            text = "change\n" + str(current_player.possible_trades[prod]) + ":1"
            self.change_buttons.append(Button((self.main_panel_x + dist_between_buttons*i + 10, 350), button_w, 50, (145, 122, 101), text, prod))

    def display_ports(self):
        for ports_c in self.corners_ports:
            self.display_port(ports_c, self.corners_ports[ports_c])

    def display_change_panel(self):
        for button in self.change_buttons:
            filename = "Graphic//" + button.destination + "_icon.png"
            img = pygame.image.load(filename)
            img = pygame.transform.scale(img, (int(button.width), int(button.width)))
            self.screen.blit(img, (button.pos[0], button.pos[1] - button.width - 5))
            button.display(self.screen)

    def display_port(self, c_t, type):
        corner1 = self.corners[c_t[0]]
        corner2 = self.corners[c_t[1]]
        pos_x = corner1.pos_x
        pos_y = corner2.pos_y
        rotation = 0
        if corner1.pos_x < corner2.pos_x and corner1.pos_y < corner2.pos_y:
            pos_x = corner1.pos_x + 5
            pos_y = corner2.pos_y - 70
            rotation = -30

        if corner1.pos_x > corner2.pos_x and corner1.pos_y > corner2.pos_y:
            pos_x = corner1.pos_x - 72
            pos_y = corner2.pos_y + 4
            rotation = 150

        if corner1.pos_x > corner2.pos_x and corner1.pos_y < corner2.pos_y:
            pos_x = corner2.pos_x - 20
            pos_y = corner1.pos_y - 42
            rotation = 30

        if corner1.pos_x < corner2.pos_x and corner1.pos_y > corner2.pos_y:
            pos_x = corner1.pos_x - 72
            pos_y = corner2.pos_y + 4
            rotation = 30

        if corner1.pos_x < corner2.pos_x and corner1.pos_y > corner2.pos_y:
            pos_x = corner1.pos_x + 5
            pos_y = corner2.pos_y + 2
            rotation = -150

        if corner1.pos_x == corner2.pos_x:
            if corner1.pos_y > corner2.pos_y:
                pos_x = corner1.pos_x + 2
                pos_y = corner2.pos_y + 5
                rotation = -90

            if corner1.pos_y < corner2.pos_y:
                pos_x = corner1.pos_x - 50
                pos_y = corner2.pos_y - 52
                rotation = 90

        filename = "Graphic//port_" + type + ".png"
        img = pygame.image.load(filename)
        img = pygame.transform.scale(img, (50, 50))
        img = pygame.transform.rotate(img, rotation)
        self.screen.blit(img, (pos_x, pos_y))

    def init_players(self, players_am):
        for i in range(players_am):
            self.buildings_spots[i] = {"town": [], "village": [], "road": []}

    def init_fields(self):
        for i in range(19):
            if fields[i] != 9:
                self.fields.append(Field(i, fields[i], numbs[i]))
            else:
                numbs.insert(i, -1)
                self.fields.append(Field(i, fields[i], 0))

    def init_corners(self):
        for i in range(self.spots):
            if i % 2 == 0:
                if i < 7:
                    pos_x = int(self.pos_start_x + i*self.edge_length*sqrt(3)/2 + 2*self.edge_length*sqrt(3)/2)
                    pos_y = int(self.pos_start_y + self.edge_length/2)
                    self.corners.append(Corner(i, pos_x, pos_y, 1))
                elif 7 < i < 16:
                    pos_x = int(self.pos_start_x + (i-8)*self.edge_length*sqrt(3)/2 + 2*self.edge_length*sqrt(3)/2)
                    pos_y = int(self.pos_start_y + self.edge_length + self.edge_length/2)
                    self.corners.append(Corner(i, pos_x, pos_y, 1))
                elif 16 <= i <= 26:
                    pos_x = int(self.pos_start_x + (i-16)*self.edge_length*sqrt(3)/2)
                    pos_y = int(self.pos_start_y + self.edge_length * 3 + self.edge_length/2)
                    self.corners.append(Corner(i, pos_x, pos_y, 1))
                elif 28 <= i <= 36:
                    pos_x = int(self.pos_start_x + (i-27)*self.edge_length*sqrt(3)/2)
                    pos_y = int(self.pos_start_y + self.edge_length * 5)
                    self.corners.append(Corner(i, pos_x, pos_y, 1))
                elif 38 <= i <= 46:
                    pos_x = int(self.pos_start_x + (i-37)*self.edge_length*sqrt(3)/2)
                    pos_y = int(self.pos_start_y + self.edge_length * 6)
                    self.corners.append(Corner(i, pos_x, pos_y, 1))
                elif 48 <= i <= 54:
                    pos_x = int(self.pos_start_x + (i-45)*self.edge_length*sqrt(3)/2)
                    pos_y = int(self.pos_start_y + self.edge_length * 8)
                    self.corners.append(Corner(i, pos_x, pos_y, 1))
            else:
                if i < 7:
                    pos_x = int(self.pos_start_x + i*self.edge_length*sqrt(3)/2 + 2*self.edge_length*sqrt(3)/2)
                    pos_y = int(self.pos_start_y)
                    self.corners.append(Corner(i, pos_x, pos_y))
                elif 7 <= i <= 15:
                    pos_x = int(self.pos_start_x + (i-6)*self.edge_length*sqrt(3)/2)
                    pos_y = int(self.pos_start_y + 2 * self.edge_length)
                    self.corners.append(Corner(i, pos_x, pos_y))
                elif 16 < i < 26:
                    pos_x = int(self.pos_start_x + (i-16)*self.edge_length*sqrt(3)/2)
                    pos_y = int(self.pos_start_y + 3 * self.edge_length)
                    self.corners.append(Corner(i, pos_x, pos_y))
                elif 27 <= i <= 37:
                    pos_x = int(self.pos_start_x + (i-27)*self.edge_length*sqrt(3)/2)
                    pos_y = int(self.pos_start_y + 4 * self.edge_length + self.edge_length/2)
                    self.corners.append(Corner(i, pos_x, pos_y,))
                elif 38 < i < 46:
                    pos_x = int(self.pos_start_x + (i-37)*self.edge_length*sqrt(3)/2)
                    pos_y = int(self.pos_start_y + 6.5 * self.edge_length)
                    self.corners.append(Corner(i, pos_x, pos_y))
                elif 46 < i < 54:
                    pos_x = int(self.pos_start_x + (i-45)*self.edge_length*sqrt(3)/2)
                    pos_y = int(self.pos_start_y + 7.5 * self.edge_length)
                    self.corners.append(Corner(i, pos_x, pos_y))

    def init_edges(self):
        for i in range(self.spots):
            for corner in self.corners_corners_map[i]:
                if self.check_if_edge_already_exist(i, corner) is False:
                    pos_1 = (self.corners[i].pos_x, self.corners[i].pos_y)
                    pos_2 = (self.corners[corner].pos_x, self.corners[corner].pos_y)
                    self.edges[(i, corner)] = (Edge(i, corner, pos_1, pos_2))

    def check_if_edge_already_exist(self, start, end):
        for edge in self.edges:
            if (start, end) == edge or (end, start) == edge:
                return True
        return False

    def find_corners_by_numb(self, numb):
        field_tags = [n for n in self.fields if self.fields[n].number is numb]
        corners = 0
        for field in field_tags:
            corners += self.fields_corners_map[field]
        return corners

    def display_corners(self):
        for corner in self.corners:
            corner.display(self.screen)

    def display_edges(self):
        for edge in self.edges:
            self.edges[edge].display(self.screen)

    def display_fields(self):
        for field in self.fields:
            p = []
            corners = self.fields_corners_map[field.tag]
            for i in corners:
                p.append((self.corners[i].pos_x, self.corners[i].pos_y))
            field.display(self.screen, (p[0], p[1], p[2], p[3], p[4], p[5]))

    def display_village(self, position, color):
        filename = "Graphic//village_" + image_name[color] + ".png"
        img = pygame.image.load(filename)
        img = pygame.transform.scale(img, (50, 50))
        self.screen.blit(img, (position[0]-25, position[1]-25))

    def display_town(self, position, color):
        filename = "Graphic//town_" + image_name[color] + ".png"
        img = pygame.image.load(filename)
        img = pygame.transform.scale(img, (50, 50))
        self.screen.blit(img, (position[0]-25, position[1]-25))

    def display_road(self, position, color):
        pygame.draw.rect(self.screen, color, pygame.Rect(position, (30, 5)))

    def display_buildings(self):
        for player in self.buildings_spots:
            for building_type in self.buildings_spots[player]:
                for corner in self.buildings_spots[player][building_type]:
                    if building_type != "road":
                        pos = (self.corners[corner].pos_x, self.corners[corner].pos_y)
                        if building_type == "village":
                            self.display_village(pos, player)
                        if building_type == "town":
                            self.display_town(pos, player)

    def display_bottom_panel(self, player):
        pygame.draw.line(self.screen, color[player.color], (0, self.screen_h - 20), (self.screen_w, self.screen_h - 20), 40)
        pygame.draw.line(self.screen, (138, 115, 73), (0, self.screen_h-42), (self.screen_w, self.screen_h - 42), 4)
        pos_x = 5
        for name in types_names:
            filename = "Graphic//" + name + "_icon.png"
            img = pygame.image.load(filename)
            img = pygame.transform.scale(img, (30, 30))
            text = pygame.font.SysFont(None, 40)
            numb = text.render(str(player.products[name]), True, (0, 0, 0))
            self.screen.blit(img, (pos_x, self.screen_h - 35))
            self.screen.blit(numb, (pos_x + 40, self.screen_h - 35))
            pos_x += 100
        for i, name in enumerate(dev_cards_names):
            filename = "Graphic//" + name + "_icon.png"
            img = pygame.image.load(filename)
            img = pygame.transform.scale(img, (30, 30))
            text = pygame.font.SysFont(None, 40)
            numb = text.render(str(player.development_cards[name]), True, (0, 0, 0))
            self.screen.blit(img, (self.screen_w - 80 - i * 100, self.screen_h - 35))
            self.screen.blit(numb, (self.screen_w - 40 - i * 100, self.screen_h - 35))


    def display_main_panel(self, player, clicked, dice_1, dice_2, init=False):
        x_pos_start = self.main_panel_x
        pygame.draw.rect(self.screen, (209, 176, 115), (x_pos_start, 0, self.screen_w, self.screen_h-39))
        pygame.draw.line(self.screen, (138, 115, 73), (x_pos_start, 0), (x_pos_start, self.screen_h), 4)
        dice1_file = "Graphic//dice_" + str(dice_1) + ".png"
        dice2_file = "Graphic//dice_" + str(dice_2) + ".png"
        dice1 = pygame.image.load(dice1_file)
        dice2 = pygame.image.load(dice2_file)
        if init is False:
            self.screen.blit(dice1, (x_pos_start + 25, 25))
            self.screen.blit(dice2, (x_pos_start + 80, 25))
            self.display_change_panel()
        self.display_message()
        self.option_button.display(self.screen, init)
        self.end_button.display(self.screen)


    def display_message(self):
        x_pos_start = self.pos_start_x + 12 * self.edge_length * sqrt(3) / 2
        text = pygame.font.SysFont(None, 34)
        text = text.render(self.message, True, (0, 0, 0))
        self.blit_text(self.message, (x_pos_start + 135, 15))

    def blit_text(self, text, pos_start):
        words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
        font = pygame.font.SysFont(None, 35)
        space = font.size(' ')[0]  # The width of a space.
        max_width = self.screen_w - 10
        max_height = pos_start[1]

        x, y = pos_start
        for line in words:
            for word in line:
                word_surface = font.render(word, 0, (0, 0, 0))
                word_width, word_height = word_surface.get_size()
                if x + word_width >= max_width:
                    x = pos_start[0]  # Reset the x.
                    y += word_height  # Start on new row.
                self.screen.blit(word_surface, (x, y))
                x += word_width + space
            x = pos_start[0]  # Reset the x.
            y += word_height  # Start on new row.

    def display(self, current_player, clicked, dice_result_1, dice_result_2, init=False):
        self.screen.fill((176, 224, 230))
        self.display_fields()
        self.display_edges()
        self.display_corners()
        self.display_ports()
        self.display_main_panel(current_player, clicked,
                                      dice_result_1, dice_result_2, init)
        self.display_bottom_panel(current_player)

    def display_end(self, current_player, winner):
        self.screen.fill((176, 224, 230))
        self.display_fields()
        self.display_edges()
        self.display_corners()
        self.display_ports()

        x_pos_start = self.main_panel_x
        pygame.draw.rect(self.screen, (209, 176, 115), (x_pos_start, 0, self.screen_w, self.screen_h-39))
        pygame.draw.line(self.screen, (138, 115, 73), (x_pos_start, 0), (x_pos_start, self.screen_h), 4)
        self.display_bottom_panel(current_player)

        msg = "YOU WON" if winner == current_player.color else "PLAYER " + current_player.color + " WON"
        font = pygame.font.SysFont(None, 70)
        text = font.render(msg, True, (255, 255, 255))
        self.screen.blit(text, ((self.screen_w - self.main_panel_x)/2 - text.get_rect().width/2, 250))




