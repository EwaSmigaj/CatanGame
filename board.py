from field import *
from vertex import *
from edge import *
from button import *
import random
from math import sqrt
from optionbutton import *
from player import Player

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
vertices_fields = {
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
vert_vert = {
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
vertices_ports = {
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
vertices_pos = []
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
    def __init__(self, players_am, ai, screen_w=1200, screen_h=720, vertices_ports=vertices_ports, fields_map=vertices_fields, vertices_map=vert_vert, spots=spots):
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.ai = ai
        self.pos_start_x = 100
        self.pos_start_y = 100
        self.dice = [0, 0]
        self.spots = spots
        self.fields = []
        self.vertices = []
        self.edges = {}
        self.players = []
        self.init = True
        self.buildings_spots = {}
        self.fields_vertices_map = fields_map
        self.vert_vert_map = vertices_map
        self.vertices_ports = vertices_ports
        self.message = "what do you want to do?"
        self.edge_length = (5 / 6 * self.screen_h) / 10
        self.main_panel_x = self.pos_start_x + 12 * self.edge_length * sqrt(3) / 2
        # self.trade_buttons = OptionButton((self.screen_w - 400, self.screen_h - 250), 100, 40, "trade", "trade")
        self.init_players(players_am)
        self.init_fields()
        self.init_vertices()
        self.init_edges()
        self.history = []
        self.current_player = self.players[0]
        self.moves_in_current_turn = {"village": [], "town": [], "road": [], "development card": []}
        self.development_cards = {"knight": 20, "victory_point": 5}
        self.last_move = 0
        self.history = []


    def roll(self):
        self.dice[0] = random.randint(1, 6)
        self.dice[1] = random.randint(1, 6)

        if sum(self.dice) == 7:
            self.take_away_products()
        self.set_message("what do you want to do?")

    def init_distribute_resources(self):
        for player in self.players:
            for village in self.buildings_spots[player.color]["village"]:
                for field in self.fields:
                    if village in self.fields_vertices_map[field.tag]:
                        player.gain(field.type, 1)

    def change_current_player(self, current_player):
        self.current_player = current_player

    def distribute_resources(self, result):
        fields_to_distribute = []
        for field in self.fields:
            if len(fields_to_distribute) >= 2:
                break
            if field.number == result:
                fields_to_distribute.append(field)
        for player in self.players:
            for village_numb in self.buildings_spots[player.color]["village"]:
                for field in fields_to_distribute:
                    if village_numb in self.fields_vertices_map[field.tag]:
                        player.gain(field.type, 1)
            for town_numb in self.buildings_spots[player.color]["town"]:
                for field in fields_to_distribute:
                    if town_numb in self.fields_vertices_map[field.tag]:
                        player.gain(field.type, 2)

    def take_away_products(self):
        for player in self.players:
            if player.cards_total > 7:
                if player.development_cards["knight"] <= 0:
                    taken = 0
                    while taken < player.cards_total // 2:
                        prod = random.choice(list(player.products.keys()))
                        if player.products[prod] > 0:
                            player.products[prod] -= 1
                            taken += 1
                else:
                    player.development_cards["knight"] -= 1

    def next_player(self):
        if self.init is False:
            if self.current_player.color == self.players[-1].color:
                self.current_player = self.players[0]
            else:
                self.current_player = self.players[self.current_player.color + 1]
            self.moves_in_current_turn = {"village": [], "town": [], "road": [], "development card": []}
        else:
            built_roads = [p.built["road"] for p in self.players]
            if set(built_roads) == {2}:
                self.init = False
                self.init_distribute_resources()
                self.current_player = self.players[0]
            elif self.current_player.color == self.players[-1].color and self.current_player.built["road"] == 1:
                self.current_player = self.players[-1]
            elif 0 in built_roads:
                self.current_player = self.players[self.current_player.color + 1]
            elif 0 not in built_roads:
                self.current_player = self.players[self.current_player.color - 1]

            self.moves_in_current_turn = {"village": [], "town": [], "road": [], "development card": []}

    def return_next_state(self, move):
        pass

    def init_players(self, players_am):
        if self.ai is False:
            for i in range(players_am):
                self.buildings_spots[i] = {"town": [], "village": [], "road": []}
                self.players.append(Player(i))
        if self.ai is True:
            for i in range(players_am):
                self.buildings_spots[i] = {"town": [], "village": [], "road": []}
                if i == -1:
                    self.players.append(Player(i))
                else:
                    self.players.append(Player(i, True))

    def init_fields(self):
        for i in range(19):
            if fields[i] != 9:
                self.fields.append(Field(i, fields[i], numbs[i]))
            else:
                numbs.insert(i, -1)
                self.fields.append(Field(i, fields[i], 0))

    def init_vertices(self):
        for i in range(self.spots):
            if i % 2 == 0:
                if i < 7:
                    pos_x = int(self.pos_start_x + i*self.edge_length*sqrt(3)/2 + 2*self.edge_length*sqrt(3)/2)
                    pos_y = int(self.pos_start_y + self.edge_length/2)
                    self.vertices.append(Vertex(i, pos_x, pos_y, 1))
                elif 7 < i < 16:
                    pos_x = int(self.pos_start_x + (i-8)*self.edge_length*sqrt(3)/2 + 2*self.edge_length*sqrt(3)/2)
                    pos_y = int(self.pos_start_y + self.edge_length + self.edge_length/2)
                    self.vertices.append(Vertex(i, pos_x, pos_y, 1))
                elif 16 <= i <= 26:
                    pos_x = int(self.pos_start_x + (i-16)*self.edge_length*sqrt(3)/2)
                    pos_y = int(self.pos_start_y + self.edge_length * 3 + self.edge_length/2)
                    self.vertices.append(Vertex(i, pos_x, pos_y, 1))
                elif 28 <= i <= 36:
                    pos_x = int(self.pos_start_x + (i-27)*self.edge_length*sqrt(3)/2)
                    pos_y = int(self.pos_start_y + self.edge_length * 5)
                    self.vertices.append(Vertex(i, pos_x, pos_y, 1))
                elif 38 <= i <= 46:
                    pos_x = int(self.pos_start_x + (i-37)*self.edge_length*sqrt(3)/2)
                    pos_y = int(self.pos_start_y + self.edge_length * 6)
                    self.vertices.append(Vertex(i, pos_x, pos_y, 1))
                elif 48 <= i <= 54:
                    pos_x = int(self.pos_start_x + (i-45)*self.edge_length*sqrt(3)/2)
                    pos_y = int(self.pos_start_y + self.edge_length * 8)
                    self.vertices.append(Vertex(i, pos_x, pos_y, 1))
            else:
                if i < 7:
                    pos_x = int(self.pos_start_x + i*self.edge_length*sqrt(3)/2 + 2*self.edge_length*sqrt(3)/2)
                    pos_y = int(self.pos_start_y)
                    self.vertices.append(Vertex(i, pos_x, pos_y))
                elif 7 <= i <= 15:
                    pos_x = int(self.pos_start_x + (i-6)*self.edge_length*sqrt(3)/2)
                    pos_y = int(self.pos_start_y + 2 * self.edge_length)
                    self.vertices.append(Vertex(i, pos_x, pos_y))
                elif 16 < i < 26:
                    pos_x = int(self.pos_start_x + (i-16)*self.edge_length*sqrt(3)/2)
                    pos_y = int(self.pos_start_y + 3 * self.edge_length)
                    self.vertices.append(Vertex(i, pos_x, pos_y))
                elif 27 <= i <= 37:
                    pos_x = int(self.pos_start_x + (i-27)*self.edge_length*sqrt(3)/2)
                    pos_y = int(self.pos_start_y + 4 * self.edge_length + self.edge_length/2)
                    self.vertices.append(Vertex(i, pos_x, pos_y, ))
                elif 38 < i < 46:
                    pos_x = int(self.pos_start_x + (i-37)*self.edge_length*sqrt(3)/2)
                    pos_y = int(self.pos_start_y + 6.5 * self.edge_length)
                    self.vertices.append(Vertex(i, pos_x, pos_y))
                elif 46 < i < 54:
                    pos_x = int(self.pos_start_x + (i-45)*self.edge_length*sqrt(3)/2)
                    pos_y = int(self.pos_start_y + 7.5 * self.edge_length)
                    self.vertices.append(Vertex(i, pos_x, pos_y))

    def init_edges(self):
        for i in range(self.spots):
            for vertex in self.vert_vert_map[i]:
                if self.check_if_edge_already_exist(i, vertex) is False:
                    pos_1 = (self.vertices[i].pos_x, self.vertices[i].pos_y)
                    pos_2 = (self.vertices[vertex].pos_x, self.vertices[vertex].pos_y)
                    self.edges[(i, vertex)] = (Edge(i, vertex, pos_1, pos_2))

    def check_if_edge_already_exist(self, start, end):
        for edge in self.edges:
            if (start, end) == edge or (end, start) == edge:
                return True
        return False

    def find_vertices_by_numb(self, numb):
        field_tags = [n for n in self.fields if self.fields[n].number is numb]
        vertices = 0
        for field in field_tags:
            vertices += self.fields_vertices_map[field]
        return vertices

    def set_message(self, msg):
        self.message = msg

    def is_end(self):
        players_score = {}
        for player in self.players:
            players_score[player.color] = player.score
            if player.score >= 6:
                return player.color
        return False

    def state_json(self):
        if self.last_move == 0:
            last = 0
        else:
            last = self.last_move[0]
            if last == "road":
                last = self.last_move[1].vertices
            elif last == "town" or last == "village":
                last = self.last_move[1].numb
            elif last == "change":
                last = self.last_move[1]
        json = {
            "current_player": self.current_player.color,
            "building_spots": self.buildings_spots,
            "players": {},
            # "dice": self.dice,
            "init": self.init,
            "current_turn": self.moves_in_current_turn,
            "last_move": last
        }
        for player in self.players:
            json["players"][player.color] = {"av_buildings": player.available_buildings,
                                             "built": player.built,
                                             # "products": player.products,
                                             "possible_trades": player.possible_trades,
                                             # "development_cards": sum(player.development_cards[i] for i in player.development_cards),
                                             # "score": player.score,
                                             "cards_total": player.cards_total,
                                             "ai": player.ai}
        return json

    def __eq__(self, other):
        if not isinstance(other, Board):
            return NotImplemented
        return self.state_json() == other.state_json()

    def __hash__(self):
        return hash(frozenset(self.state_json()))

