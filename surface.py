import pygame
from board import Board
from vertex import *
from optionbutton import OptionButton
from button import Button



class Surface:
    def __init__(self, board_inst, screen_w=1200, screen_h=720):
        self.board = board_inst
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.pos_start_x = self.board.pos_start_x
        self.pos_start_y = self.board.pos_start_y
        self.screen = pygame.display.set_mode((screen_w, screen_h))
        self.types_names = ["wood", "clay", "sheep", "hay", "rock"]
        self.dev_cards_names = ["knight", "victory_point"]
        self.main_panel_x = self.pos_start_x + 12*self.board.edge_length*sqrt(3)/2
        self.option_button = OptionButton((self.main_panel_x + (self.screen_w - self.main_panel_x) / 2 - 100, 100), 200,
                                          50, (124, 134, 123))
        self.end_button = Button((self.screen_w - 400, self.screen_h - 150), 150, 50, (124, 134, 123), "end ture",
                                 "end")
        self.change_buttons = [0, 0, 0, 0, 0]
        self.init_change_buttons(self.board.current_player)


    def init_change_buttons(self, current_player):
        dist_between_buttons = (self.screen_w - self.main_panel_x) / 5
        button_w = dist_between_buttons - 20
        for i, prod in enumerate(current_player.possible_trades):
            text = "change\n" + str(current_player.possible_trades[prod]) + ":1"
            self.change_buttons[i] = (Button((self.main_panel_x + dist_between_buttons*i + 10, 350), button_w, 50, (145, 122, 101), text, prod))

    def display_corners(self):
        for corner in self.board.vertices:
            corner.display(self.screen)

    def display_edges(self):
        for edge in self.board.edges:
            self.board.edges[edge].display(self.screen)

    def display_fields(self):
        for field in self.board.fields:
            p = []
            corners = self.board.fields_vertices_map[field.tag]
            for i in corners:
                p.append((self.board.vertices[i].pos_x, self.board.vertices[i].pos_y))
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
        for player in self.board.buildings_spots:
            for building_type in self.board.buildings_spots[player]:
                for corner in self.board.buildings_spots[player][building_type]:
                    if building_type != "road":
                        pos = (self.board.vertices[corner].pos_x, self.board.vertices[corner].pos_y)
                        if building_type == "village":
                            self.display_village(pos, player)
                        if building_type == "town":
                            self.display_town(pos, player)

    def display_bottom_panel(self, player):
        pygame.draw.line(self.screen, color[player.color], (0, self.screen_h - 20), (self.screen_w, self.screen_h - 20), 40)
        pygame.draw.line(self.screen, (138, 115, 73), (0, self.screen_h-42), (self.screen_w, self.screen_h - 42), 4)
        pos_x = 5

        for name in self.types_names:
            filename = "Graphic//" + name + "_icon.png"
            img = pygame.image.load(filename)
            img = pygame.transform.scale(img, (30, 30))
            text = pygame.font.SysFont(None, 40)
            numb = text.render(str(player.products[name]), True, (0, 0, 0))
            self.screen.blit(img, (pos_x, self.screen_h - 35))
            self.screen.blit(numb, (pos_x + 40, self.screen_h - 35))
            pos_x += 100
        for i, name in enumerate(self.dev_cards_names):
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
        if init is False and dice_1 != 0:

            dice1_file = "Graphic//dice_" + str(dice_1) + ".png"
            dice2_file = "Graphic//dice_" + str(dice_2) + ".png"
            dice1 = pygame.image.load(dice1_file)
            dice2 = pygame.image.load(dice2_file)
            self.screen.blit(dice1, (x_pos_start + 25, 25))
            self.screen.blit(dice2, (x_pos_start + 80, 25))
        if player.ai is False or init is True:
            if init is False:
                self.display_change_panel()
            self.display_message()
            self.option_button.display(self.screen, init)
            self.end_button.display(self.screen)
        elif player.ai is True and init is False:
            msg = "AI MOVE"
            text = pygame.font.SysFont(None, 34)
            text = text.render(msg, True, (0, 0, 0))
            self.screen.blit(text, (x_pos_start + 25, 80))

    def display_message(self):
        x_pos_start = self.board.pos_start_x + 12 * self.board.edge_length * sqrt(3) / 2
        text = pygame.font.SysFont(None, 34)
        text = text.render(self.board.message, True, (0, 0, 0))
        self.blit_text(self.board.message, (x_pos_start + 135, 15))

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

    def display_ports(self):
        for ports_c in self.board.vertices_ports:
            self.display_port(ports_c, self.board.vertices_ports[ports_c])

    def display_change_panel(self):
        for button in self.change_buttons:
            filename = "Graphic//" + button.destination + "_icon.png"
            img = pygame.image.load(filename)
            img = pygame.transform.scale(img, (int(button.width), int(button.width)))
            self.screen.blit(img, (button.pos[0], button.pos[1] - button.width - 5))
            button.display(self.screen)

    def display_port(self, c_t, type):
        corner1 = self.board.vertices[c_t[0]]
        corner2 = self.board.vertices[c_t[1]]
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

    def display(self, current_player, clicked, dice_result_1, dice_result_2, init=False):
        self.screen.fill((176, 224, 230))
        # print(init)
        self.display_fields()
        self.display_edges()
        self.display_corners()
        self.display_ports()
        self.display_main_panel(current_player, clicked,
                                      dice_result_1, dice_result_2, init)
        self.display_bottom_panel(current_player)

    def display_end(self, current_player, winner):


        msg = "YOU WON" if winner == current_player.color else "PLAYER " + str(winner) + " WON"
        font = pygame.font.SysFont(None, 70)
        text = font.render(msg, True, (255, 255, 255))
        self.screen.blit(text, (self.main_panel_x + 30, 550))
