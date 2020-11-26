from board import *
from player import *
from catanmoves import *
from edge import Edge
import random
import pygame
import sys


class Game:
    def __init__(self, numb_of_players):
        self.players = []
        self.init_players(numb_of_players)
        self.board = Board(numb_of_players)
        self.just_started = True
        self.action = CatanMoves(self.board)
        self.dice_result_1 = 1
        self.dice_result_2 = 1
        self.clicked = None
        self.next_turn = False
        self.moves_in_current_turn = {"village": [], "town": [], "road": [], "development card": []}  # pos
    def init_players(self, numb_of_players):
        for i in range(numb_of_players):
            self.players.append(Player(i))

    def turn(self, player):
        self.action.change_current_player(player)
        available_act = self.action.return_available_board_actions()

    def check_corner_clicked(self, pos, init=False):
        av_act = self.action.return_available_board_actions()["corner"] if init is False else \
        self.action.init_return_available_board_actions()["corner"]
        for corner in av_act:
            if init is False:
                if corner.is_inside(pos) is True:
                    self.unclick(init)
                    corner.click()
                    self.clicked = corner
                    self.board.option_button.change_dest(corner)
                    return True
            elif init is True:
                if corner.is_inside(pos) is True and corner.building == 0:
                    self.unclick(init)
                    corner.click()
                    self.clicked = corner
                    self.board.option_button.change_dest(corner)
                    return True
        return False

    def check_edge_clicked(self, pos, init=False):
        av_act = self.action.return_available_board_actions()["edge"] if init is False else self.action.init_return_available_board_actions()["edge"]
        for edge in av_act:
            if edge.is_inside(pos) is True:
                self.unclick(init)
                edge.click()
                self.clicked = edge
                self.board.option_button.change_dest(edge)
                return True
        return False

    def check_action_button_clicked(self, pos, init=False):
        if self.board.option_button.is_inside(pos) is True:
            self.board.option_button.click()
            # self.clicked = self.board.option_button
            self.option_button_action(self.board.option_button.destination, init)
            return True
        return False

    def check_dev_button_clicked(self, pos, init=False):
        if self.board.option_button.is_inside(pos) is True:
            self.board.dev_button.click()
            self.option_button_action(self.board.dev_button.destination, init)
            return True
        return False

    def check_change_button_clicked(self, pos):
        for button in self.board.change_buttons:
            print(f"clicked = {self.clicked}")
            if button.is_inside(pos) is True:
                print("CLICKED LOL")
                if type(self.clicked) is Button:
                    self.change_button_action(button.destination)
                else:
                    self.unclick()
                    self.clicked = button
                    button.click()
                    print(f"clicked2 = {self.clicked}")
                return True
        return False

    def change_button_action(self, change_to):
        self.action.current_player.change(self.clicked.destination, change_to)
        self.unclick()

    def check_end_button_clicked(self, pos, init=False):
        mv = self.moves_in_current_turn
        if self.board.end_button.is_inside(pos) is True:
            if init is False or init is True and len(mv["village"]) == 1 and len(mv["road"]) == 1:
                self.next_turn = True
                return True
            if init is True and (len(mv["village"]) < 1 or len(mv["road"]) < 1):
                self.board.message = "You have to build 1 road and 1 village to end this ture"
                return False
        return False

    def roll(self):
        self.dice_result_1 = random.randint(1, 6)
        self.dice_result_2 = random.randint(1, 6)
        return self.dice_result_1 + self.dice_result_2

    def init_distribute_resources(self):
        for player in self.players:
            for village in self.board.buildings_spots[player.color]["village"]:
                for field in self.board.fields:
                    if village in self.board.fields_corners_map[field.tag]:
                        player.gain(field.type, 1)

    def distribute_resources(self, result):
        fields_to_distribute = []
        for field in self.board.fields:
            if len(fields_to_distribute) >= 2:
                break
            if field.number == result:
                fields_to_distribute.append(field)
        for player in self.players:
            for village_numb in self.board.buildings_spots[player.color]["village"]:
                for field in fields_to_distribute:
                    if village_numb in self.board.fields_corners_map[field.tag]:
                        player.gain(field.type, 1)
            for town_numb in self.board.buildings_spots[player.color]["town"]:
                for field in fields_to_distribute:
                    if town_numb in self.board.fields_corners_map[field.tag]:
                        player.gain(field.type, 2)

    def option_button_action(self, destination, init=False):
        dest = {
            "village": self.action.build_village,
            "road": self.action.build_road,
            "town": self.action.build_town,
            "development card": self.action.buy_development_card
        }
        ret = None
        if destination == "development card":
            ret = dest[self.board.option_button.destination]()
        elif destination == "road":
            if init is False or (init is True and len(self.moves_in_current_turn["road"]) < 1):
                ret = dest[destination](self.clicked.corners, init)
                pos = self.clicked.corners
        else:
            if init is False or (init is True and len(self.moves_in_current_turn[destination]) < 1):
                ret = dest[destination](self.clicked.numb, init)
                pos = self.clicked.numb

        if ret is None and init is True:
            self.board.message = "You can build only one village and one road on the init phase"
        elif ret is not True and ret not in self.action.development_cards:
            self.board.message = ret
        else:
            self.moves_in_current_turn[destination].append(ret)
        self.unclick(init)

    def unclick(self, init=False):
        if self.clicked is not None:
            self.clicked.clicked = False
            self.clicked = None
        if init is True:
            self.board.option_button.change_dest(None)
        else:
            self.board.option_button.change_dest("development card")

    def is_end(self):
        for player in self.players:
            if player.score >= 10:
                return player.color
        return False

    def init_phase(self):
        turns = 0
        back = 0
        while turns < len(self.players)*2:
            self.init_turn()
            back = self.init_next_player(back)
            turns += 1
        self.init_distribute_resources()

    def undo(self):
        pass

    def click_handler(self, event, init=False):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if self.check_action_button_clicked(pos, init) is False:
                if self.check_end_button_clicked(pos, init) is False:
                    if self.check_corner_clicked(pos, init) is False:
                        if self.check_edge_clicked(pos, init) is False:
                            if self.check_change_button_clicked(pos) is False:
                                self.unclick(init)
        # self.button_action()

    def init_turn(self):
        self.board.message = "init turn, build 1 village and 1 road"
        while self.next_turn is False:
            self.board.display(self.action.current_player, self.clicked, self.dice_result_1, self.dice_result_2, True)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                self.click_handler(event, True)
        self.next_turn = False

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

    def turn(self):
        self.unclick()
        rolled = self.roll()
        self.board.init_change_buttons(self.action.current_player)
        self.board.message = "what do you want to do?"
        self.distribute_resources(rolled)
        if rolled == 7:
            self.take_away_products()
        while self.next_turn is False:
            self.board.display(self.action.current_player, self.clicked, self.dice_result_1, self.dice_result_2)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                self.click_handler(event)
        self.next_turn = False

    def next_player(self):
        if self.action.current_player.color == self.players[-1].color:
            self.action.current_player = self.players[0]
        else:
            self.action.current_player = self.players[self.action.current_player.color + 1]
        self.moves_in_current_turn = {"village": [], "town": [], "road": [], "development card": []}

    def init_next_player(self, back):
        if self.action.current_player.color == self.players[-1].color and back == 0:
            self.action.current_player = self.players[-1]
            self.moves_in_current_turn = {"village": [], "town": [], "road": [], "development card": []}
            return 1
        elif back == 0:
            self.action.current_player = self.players[self.action.current_player.color + 1]
        elif back == 1:
            self.action.current_player = self.players[self.action.current_player.color - 1]
        self.moves_in_current_turn = {"village": [], "town": [], "road": [], "development card": []}
        return back

    def run(self):
        self.action.current_player = self.players[0]
        self.init_phase()
        self.action.current_player = self.players[0]
        win = False
        while win is False:
            self.turn()
            self.next_player()
            win = self.is_end()
        self.board.display_end(self.action.current_player, win)


g = Game(1)
g.run()
