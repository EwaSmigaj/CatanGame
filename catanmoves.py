import random


class CatanMoves:
    def __init__(self, board):
        self.board = board
        self.costs = {"road": {"wood": 1, "clay": 1},
                      "village": {"wood": 1, "clay": 1, "hay": 1, "sheep": 1},
                      "town": {"rock": 3, "hay": 2},
                      "development_card": {"rock": 1, "hay": 1, "sheep": 1}}
        self.development_cards = {"knight": 20, "victory_point": 5}
        self.current_player = None

    def return_available_board_actions(self):
        av_act = {"corner": [], "edge": []}
        buildings_spots = self.board.buildings_spots[self.current_player.color]
        # check corners
        for corner in self.board.corners:
            if corner.empty is True and corner.available is True:
                road_connection = [x for x in buildings_spots["road"] if corner.numb in x]
                # print(f"corner = {corner.numb} road conntecton = {road_connection}")
                if len(road_connection) > 0:
                    av_act["corner"].append(corner)
            elif corner.empty is False and corner.building == 1 and corner.color == self.current_player.color:
                av_act["corner"].append(corner)

        # check edges near buildings
        for edge in self.board.edges:
            e = -1
            if edge[0] in buildings_spots["town"] or edge[0] in buildings_spots["village"]:
                e = edge[0]
            elif edge[1] in buildings_spots["town"] or edge[1] in buildings_spots["village"]:
                e = edge[1]
            if e != -1:
                for corner in self.board.corners_corners_map[e]:
                    if self.select_edge(e, corner).available is True:
                        if self.select_edge(e, corner) not in av_act["edge"]:
                            av_act["edge"].append(self.select_edge(e, corner))

        # check edges near road
        for road in buildings_spots["road"]:
            for road_c in road:
                for corner in self.board.corners_corners_map[road_c]:
                    edge = self.select_edge(corner, road_c)
                    if edge.available is True and edge not in av_act["edge"]:
                        av_act["edge"].append(edge)
        return av_act

    def init_return_available_board_actions(self):
        av_act = {"corner": [], "edge": []}
        buildings_spots = self.board.buildings_spots[self.current_player.color]
        for corner in self.board.corners:
            if corner.empty is True and corner.available is True:
                av_act["corner"].append(corner)
        for edge in self.board.edges:
            e = -1
            if edge[0] in buildings_spots["town"] or edge[0] in buildings_spots["village"]:
                e = edge[0]
            elif edge[1] in buildings_spots["town"] or edge[1] in buildings_spots["village"]:
                e = edge[1]
            if e != -1:
                for corner in self.board.corners_corners_map[e]:
                    if self.select_edge(e, corner).available is True:
                        if self.select_edge(e, corner) not in av_act["edge"]:
                            av_act["edge"].append(self.select_edge(e, corner))

        # print(av_act["corner"])
        return av_act

    def select_edge(self, val1, val2):
        y = [x for x in self.board.edges if val1 in x and val2 in x]
        return self.board.edges[y[0]]

    def update_board_availability(self, corner_numb):
        corners_to_block = self.board.corners_corners_map[corner_numb]
        for corner_numb in corners_to_block:
            self.board.corners[corner_numb].available = 0

    def build_road(self, position, free=False):
        building_type = "road"
        if self.current_player.available_buildings[building_type] < 1:
            return "You don't have any road to build"
        if free is False:
            if self.current_player.remove_resources(self.costs[building_type]) is False:
                return "You don't have enough resources"
        position = self.select_edge(position[0], position[1])
        position.available = False
        position.color = self.current_player.color
        self.current_player.built[building_type] += 1
        self.current_player.available_buildings[building_type] -= 1
        self.board.buildings_spots[self.current_player.color][building_type].append(position.corners)
        return True

    def build_village(self, position, free=False):
        building_type = "village"
        if self.current_player.available_buildings[building_type] < 1:
            return "You don't have any village to build"
        if free is False:
            if self.current_player.remove_resources(self.costs[building_type]) is False:
                return "You don't have enough resources"
        position = self.board.corners[position]
        position.available = False
        position.empty = False
        position.building = 1
        position.color = self.current_player.color
        self.current_player.built[building_type] += 1
        self.current_player.available_buildings[building_type] -= 1
        self.board.buildings_spots[self.current_player.color][building_type].append(position.numb)
        self.actualize_trades(position)
        self.update_board_availability(position.numb)
        return True

    def build_town(self, position, free=False):
        building_type = "town"
        if self.current_player.available_buildings[building_type] < 1:
            return "You don't have any town to build"
        if self.current_player.remove_resources(self.costs[building_type]) is False:
            return "You don't have enough resources"
        position = self.board.corners[position]
        position.building = 2
        self.current_player.built[building_type] += 1
        self.current_player.built["village"] -= 1
        self.current_player.available_buildings["village"] += 1
        self.current_player.available_buildings[building_type] -= 1
        self.board.buildings_spots[self.current_player.color][building_type].append(position.numb)
        index = self.board.buildings_spots[self.current_player.color]["village"].index(position.numb)
        del self.board.buildings_spots[self.current_player.color]["village"][index]
        self.update_board_availability(position.numb)
        return True

    def buy_development_card(self):
        # print("DEV CARD")
        if self.current_player.remove_resources(self.costs["development_card"]) is False:
            # print("You don't have enough resources")
            return "You don't have enough resources"
        all_cards = []
        for dev_card_type in self.development_cards:
            for _ in range(self.development_cards[dev_card_type]):
                all_cards.append(dev_card_type)
        if all_cards == 0:
            # print("There's no resource card in bank")
            return "There's no resource card in bank"
        random.shuffle(all_cards)
        self.current_player.development_cards[all_cards[0]] += 1
        return all_cards[0]

    def change_current_player(self, current_player):
        self.current_player = current_player

    def trade(self, player):
        pass

    def actualize_trades(self, position):
        for port_pos in self.board.corners_ports:
            print(port_pos)
            print(f"POSITION = {position.numb}")
            if position.numb in port_pos:
                product = self.board.corners_ports[port_pos]
                self.current_player.possible_trades[product] = 2

