import random


class CatanMoves:
    def __init__(self, board):
        self.board = board
        self.costs = {"road": {"wood": 1, "clay": 1},
                      "village": {"wood": 1, "clay": 1, "hay": 1, "sheep": 1},
                      "town": {"rock": 3, "hay": 2},
                      "development card": {"rock": 1, "hay": 1, "sheep": 1}}
        self.development_cards = {"knight": 20, "victory_point": 5}
        self.init = True
        self.next_turn = False

    def next_turn(self):
        self.next_turn = True

    def return_available_board_actions(self):
        av_act = {"corner": [], "edge": []}
        buildings_spots = self.board.buildings_spots[self.board.current_player.color]
        # check corners
        for corner in self.board.corners:
            if corner.empty is True and corner.available is True:
                road_connection = [x for x in buildings_spots["road"] if corner.numb in x]
                if len(road_connection) > 0:
                    av_act["corner"].append(corner)
            elif corner.empty is False and corner.building == 1 and corner.color == self.board.current_player.color:
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

    def legal_plays(self):
        player = self.board.current_player
        actions = []
        buildings_spots = self.board.buildings_spots[player.color]

        if self.board.init is True:
            if len(self.board.moves_in_current_turn["road"]) == 1:
                actions.append((self.board.current_player.color, ("end", 0)))

            elif player.built["village"] == 0 or (player.built["village"] == player.built["road"] and
            self.board.moves_in_current_turn == {"village": [], "town": [], "road": [], "development card": []}):
                for corner in self.board.corners:
                    if corner.empty is True and corner.available is True:
                        actions.append((player.color, ("village", corner.numb)))

            else:
                for edge in self.board.edges:
                    e = -1
                    if edge[0] in buildings_spots["village"]:
                        e = edge[0]
                    elif edge[1] in buildings_spots["village"]:
                        e = edge[1]
                    if e != -1:
                        for corner in self.board.corners_corners_map[e]:
                            if self.select_edge(e, corner).available is True:
                                if (player.color, ("road", self.select_edge(e, corner).corners)) not in actions:
                                    actions.append((player.color, ("road", self.select_edge(e, corner).corners)))
            return actions

        if player.can_afford(self.costs["village"]) or player.can_afford(self.costs["town"]):
            for corner in self.board.corners:
                if corner.empty is True and corner.available is True:
                    road_connection = [x for x in buildings_spots["road"] if corner.numb in x]
                    if len(road_connection) > 0 and player.can_afford(self.costs["village"]):
                        actions.append((self.board.current_player.color, ("village", corner.numb)))
                elif corner.empty is False and corner.building == 1 and corner.color == player.color and player.can_afford(self.costs["town"]):
                    actions.append((self.board.current_player.color, ("town", corner.numb)))

        # check edges near buildings
        if player.can_afford(self.costs["road"]):
            for edge in self.board.edges:
                e = -1
                if edge[0] in buildings_spots["town"] or edge[0] in buildings_spots["village"]:
                    e = edge[0]
                elif edge[1] in buildings_spots["town"] or edge[1] in buildings_spots["village"]:
                    e = edge[1]
                if e != -1:
                    for corner in self.board.corners_corners_map[e]:
                        if self.select_edge(e, corner).available is True:
                            if ((self.board.current_player.color, ("road", self.select_edge(e, corner).corners))) not in actions:
                                actions.append((self.board.current_player.color, ("road", self.select_edge(e, corner).corners)))

        # check edges near road
            for road in buildings_spots["road"]:
                for road_c in road:
                    for corner in self.board.corners_corners_map[road_c]:
                        edge = self.select_edge(corner, road_c)
                        if edge.available is True and ((self.board.current_player.color, ("road", edge.corners))) not in actions:
                            actions.append((self.board.current_player.color, ("road", edge.corners)))

    # chceck if player can change something
        for product in player.products:
            if player.can_change(product):
                for prod in player.products:
                    if prod != product:
                        actions.append((self.board.current_player.color, ("change", (product, prod))))

        if player.can_afford(self.costs["development card"]):
            actions.append((self.board.current_player.color, ("development card", 0)))

        actions.append((self.board.current_player.color, ("end", 0)))
        return actions

    def ai_move(self, move, simulation=True, init=False):
        # move = (action name, pos)
        if simulation is False:
            print(f"AI MOVE = {move}, simulation = {simulation}")
        translate_move = {
            "village": self.build_village,
            "town": self.build_town,
            "road": self.build_road,
            "development card": self.buy_development_card,
            "end": self.ai_next_turn,
            "change": self.board.current_player.change,
        }

        if move[1][1] == 0:
            if move[1][0] == "end":
                self.board.history.append(move)

            translate_move[move[1][0]](simulation)
        elif type(move[1][1]) is tuple: # road
            f = move[1][1]
            if move[1][0] == "road":
                translate_move[move[1][0]](move[1][1])
            else:
                translate_move[move[1][0]](move[1][1][0], move[1][1][1])
                self.board.last_move = move
                self.board.history.append(move)
        else:
            translate_move[move[1][0]](move[1][1])



    def ai_next_turn(self, simulation=True):
        if simulation is True:
            if self.board.init is False:
                self.board.next_player()
                self.board.roll()
                self.board.distribute_resources(sum(self.board.dice))
                self.board.last_move = ("end", 0)
            if self.board.init is True:
                self.board.next_player()
        else:
            # print("ENDDDDD")
            # print(f"current player which is ending = {self.board.current_player}")
            self.next_turn = True

    def init_return_available_board_actions(self):
        av_act = {"corner": [], "edge": []}
        buildings_spots = self.board.buildings_spots[self.board.current_player.color]
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
        if self.board.current_player.available_buildings[building_type] < 1:
            return "You don't have any road to build"
        if self.board.init is False:
            if self.board.current_player.remove_resources(self.costs[building_type]) is False:
                return "You don't have enough resources"
        position = self.select_edge(position[0], position[1])
        position.available = False
        position.color = self.board.current_player.color
        self.board.current_player.built[building_type] += 1
        self.board.current_player.available_buildings[building_type] -= 1
        self.board.buildings_spots[self.board.current_player.color][building_type].append(position.corners)
        self.board.last_move = ("road", position)
        self.board.history.append((self.board.current_player.color, ("road", position.corners)))
        self.board.moves_in_current_turn["road"].append(position.corners)
        return True

    def build_village(self, position, free=False):
        building_type = "village"
        if self.board.current_player.available_buildings[building_type] < 1:
            return "You don't have any village to build"
        if self.board.init is False:
            if self.board.current_player.remove_resources(self.costs[building_type]) is False:
                return "You don't have enough resources"
        position = self.board.corners[position]
        position.available = False
        position.empty = False
        position.building = 1
        position.color = self.board.current_player.color
        self.board.current_player.built[building_type] += 1
        self.board.current_player.available_buildings[building_type] -= 1
        self.board.buildings_spots[self.board.current_player.color][building_type].append(position.numb)
        self.actualize_trades(position)
        self.update_board_availability(position.numb)
        self.board.last_move = ("village", position)
        self.board.history.append((self.board.current_player.color, ("village", position.numb)))
        self.board.moves_in_current_turn["village"].append(position.numb)
        return True

    def build_town(self, position, free=False):
        building_type = "town"
        if self.board.current_player.available_buildings[building_type] < 1:
            return "You don't have any town to build"
        if self.board.current_player.remove_resources(self.costs[building_type]) is False:
            return "You don't have enough resources"
        position = self.board.corners[position]
        position.building = 2
        self.board.current_player.built[building_type] += 1
        self.board.current_player.built["village"] -= 1
        self.board.current_player.available_buildings["village"] += 1
        self.board.current_player.available_buildings[building_type] -= 1
        self.board.buildings_spots[self.board.current_player.color][building_type].append(position.numb)
        index = self.board.buildings_spots[self.board.current_player.color]["village"].index(position.numb)
        del self.board.buildings_spots[self.board.current_player.color]["village"][index]
        self.update_board_availability(position.numb)
        self.board.last_move = ("town", position)
        self.board.history.append((self.board.current_player.color, ("town", position.numb)))
        return True

    def buy_development_card(self, simulation=True):
        if self.board.current_player.remove_resources(self.costs["development card"]) is False:
            return "You don't have enough resources"
        all_cards = []
        for dev_card_type in self.development_cards:
            for _ in range(self.development_cards[dev_card_type]):
                all_cards.append(dev_card_type)
        if all_cards == 0:
            return "There's no resource card in bank"
        random.shuffle(all_cards)
        self.board.current_player.development_cards[all_cards[0]] += 1
        self.board.last_move = ("development card", 0)
        self.board.history.append((self.board.current_player.color, ("development card", 0)))
        return all_cards[0]

    def change_board(self, board):
        self.board = board

    def trade(self, player):
        pass

    def actualize_trades(self, position):
        for port_pos in self.board.corners_ports:
            if position.numb in port_pos:
                product = self.board.corners_ports[port_pos]
                self.board.current_player.possible_trades[product] = 2

