from board import *
from player import *
from catanmoves import *
from surface import Surface
from edge import *
import random
import pygame
import sys
from copy import deepcopy
from montecarlo import Montecarlo


class Game:
    def __init__(self, numb_of_players, ai):
        self.players = []
        self.numb_of_players = numb_of_players
        self.board = Board(self.numb_of_players, ai)
        self.surface = Surface(self.board)
        self.action = CatanMoves(self.board)
        self.ai = Montecarlo(self.board, self.action)
        self.clicked = None

    def check_corner_clicked(self, pos, init=False):
        av_act = self.action.return_available_board_actions()["corner"] if init is False else \
        self.action.init_return_available_board_actions()["corner"]
        for corner in av_act:
            if init is False:
                if corner.is_inside(pos) is True:
                    self.unclick(init)
                    corner.click()
                    self.clicked = corner
                    self.surface.option_button.change_dest(corner)
                    return True
            elif init is True:
                if corner.is_inside(pos) is True and corner.building == 0:
                    self.unclick(init)
                    corner.click()
                    self.clicked = corner
                    self.surface.option_button.change_dest(corner)
                    return True
        return False

    def check_edge_clicked(self, pos, init=False):
        av_act = self.action.return_available_board_actions()["edge"] if init is False else self.action.init_return_available_board_actions()["edge"]
        for edge in av_act:
            if edge.is_inside(pos) is True:
                self.unclick(init)
                edge.click()
                self.clicked = edge
                self.surface.option_button.change_dest(edge)
                return True
        return False

    def check_action_button_clicked(self, pos, init=False):
        if self.surface.option_button.is_inside(pos) is True:
            self.surface.option_button.click()
            # self.clicked = self.board.option_button
            self.option_button_action(self.surface.option_button.destination, init)
            return True
        return False

    def check_dev_button_clicked(self, pos, init=False):
        if self.surface.option_button.is_inside(pos) is True:
            self.surface.dev_button.click()
            self.option_button_action(self.surface.dev_button.destination, init)
            return True
        return False

    def check_change_button_clicked(self, pos, init=False):
        if init is False:
            for button in self.surface.change_buttons:
                if button.is_inside(pos) is True:
                    if type(self.clicked) is Button:
                        self.change_button_action(button.destination)
                    else:
                        self.unclick()
                        self.clicked = button
                        button.click()
                    return True
        return False

    def change_button_action(self, change_to):
        self.board.current_player.change(self.clicked.destination, change_to)
        self.board.history.append((self.board.current_player.color, ("change", (self.clicked.destination, change_to))))
        self.unclick()

    def check_end_button_clicked(self, pos, init=False):
        mv = self.board.moves_in_current_turn
        if self.surface.end_button.is_inside(pos) is True:
            if init is False or (init is True and len(mv["village"]) == 1 and len(mv["road"]) == 1):
                self.action.next_turn = True
                return True
            if init is True and (len(mv["village"]) < 1 or len(mv["road"]) < 1):
                self.board.message = "You have to build 1 road and 1 village to end this ture"
                return False
        return False

    def option_button_action(self, destination, init=False):
        dest = {
            "village": self.action.build_village,
            "road": self.action.build_road,
            "town": self.action.build_town,
            "development card": self.action.buy_development_card
        }
        ret = None
        if destination == "development card":
            ret = dest[self.surface.option_button.destination]()
        elif destination == "road":
            if init is False or (init is True and len(self.board.moves_in_current_turn["road"]) < 1):
                ret = dest[destination](self.clicked.corners, init)
                pos = self.clicked.corners
        else:
            if init is False or (init is True and len(self.board.moves_in_current_turn[destination]) < 1):
                ret = dest[destination](self.clicked.numb, init)
                pos = self.clicked.numb

        if ret is None and init is True:
            self.board.message = "You can build only one village and one road on the init phase"
        elif ret is not True and ret not in self.action.development_cards:
            self.board.message = ret
        else:
            self.board.moves_in_current_turn[destination].append(ret)
        self.unclick(init)

    def unclick(self, init=False):
        if self.clicked is not None:
            self.clicked.clicked = False
            self.clicked = None
        if init is True:
            self.surface.option_button.change_dest(None)
        else:
            self.surface.option_button.change_dest("development card")

    # def init_phase(self):
    #     turns = 0
    #     while turns < len(self.board.players)*2:
    #         self.init_turn()
    #         self.board.init_next_player()
    #         turns += 1
    #     self.board.init_distribute_resources()
    #     self.board.init = False

    def undo(self):
        pass

    def click_handler(self, event, init=False):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if self.check_action_button_clicked(pos, init) is False:
                if self.check_end_button_clicked(pos, init) is False:
                    if self.check_corner_clicked(pos, init) is False:
                        if self.check_edge_clicked(pos, init) is False:
                            if self.check_change_button_clicked(pos, init) is False:
                                self.unclick(init)

    # def init_turn(self):
    #     self.board.message = "init turn, build 1 village and 1 road"
    #     while self.action.next_turn is False:
    #         self.surface.display(self.board.current_player, self.clicked, self.board.dice[0], self.board.dice[1], True)
    #         pygame.display.flip()
    #         for event in pygame.event.get():
    #             if event.type == pygame.QUIT:
    #                 sys.exit(0)
    #             if self.board.current_player.ai is True:
    #                 self.action.ai_move(self.action.ai_move(self.ai.get_play(True), False, True))
    #             else:
    #                 self.click_handler(event, True)
    #     self.action.next_turn = False

    def turn(self):
        if self.board.init is False:
            self.unclick()
            self.board.roll()
            self.board.distribute_resources(sum(self.board.dice))
            if self.board.current_player.ai is False:
                self.surface.init_change_buttons(self.board.current_player)
        elif self.board.current_player.ai is False:
            self.board.message = "init turn, build 1 village and 1 road"
        while self.action.next_turn is False:
            self.surface.display(self.board.current_player, self.clicked, self.board.dice[0], self.board.dice[1], self.board.init)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                if self.board.current_player.ai is False:
                    self.click_handler(event)
            if self.board.current_player.ai is True:
                self.action.ai_move(self.ai.get_play())
        self.action.next_turn = False

    def run(self):
        # self.init_phase()
        self.board.init = True
        self.board.current_player = self.board.players[0]
        win = False
        while win is False:
            self.turn()
            self.board.next_player()
            win = self.board.is_end()

        while True:
            self.surface.display_end(self.board.current_player, win)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)

    def copy(self):
        copyobj = Game(self.numb_of_players)
        for name, attr in self.__dict__.items():
            if hasattr(attr, 'copy') and callable(getattr(attr, 'copy')):
                copyobj.__dict__[name] = attr.copy()
            else:
                copyobj.__dict__[name] = deepcopy(attr)
        return copyobj


g = Game(2, True)
g.run()

