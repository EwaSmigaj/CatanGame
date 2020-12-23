import datetime as datetime
from random import choice
from math import log, sqrt
from catanmoves import CatanMoves
from copy import deepcopy
from operator import itemgetter

class Montecarlo:
    def __init__(self, board, action, time=30, max_moves=35):
        self.board = board
        self.action = deepcopy(action)
        self.calculation_time = datetime.timedelta(seconds=time)
        self.max_moves = max_moves
        self.plays = {}
        self.wins = {}
        self.points = {}
        self.states = []

    def update(self, state):
        self.states.append(state)

    def get_play(self):
        print("******************************************************")
        print("******************************************************")
        print("GET PLAY")
        print("******************************************************")
        print("******************************************************")
        self.max_depth = 0
        state = self.board
        print(state.state_json())

        player = state.current_player
        print(player.products)
        if state.is_end() == player.color and state.is_end() is not False:
            return (0, ('end', 0))
        self.action.change_board(state)
        legal = self.action.legal_plays()
        print(legal)
        if len(legal) == 1:
            return legal[0]
        games = 0
        begin = datetime.datetime.utcnow()
        while datetime.datetime.utcnow() - begin < self.calculation_time:
            self.run_simulation()
            games += 1

        moves_states = [tuple(self.next_state(state, p).history) for p in legal]
        print(f"moves_states = {moves_states}")

        best = 0
        pw = 0
        p1inms = 0

        for p, w in zip(self.plays, self.wins):
            y= p
            if p[1] in moves_states:
                p1inms +=1
                # print("p1 in ms")
                if self.wins[w]/self.plays[p] > pw:
                    pw = self.wins[w]/self.plays[p]
                    best = p[1][-1]


        max_points = 0
        points = []
        if pw == 0:
            # print(f"self.points = {self.points}")
            for p in self.points:
                # print(p[1].last_move)
                if p[1] in moves_states:
                    points.append(self.points[p])
                    if self.points[p]/self.plays[p] > max_points:
                        max_points = self.points[p]
                        best = p[1][-1]

            print(f"now best = {best} (points), max points = {max_points}")
            print(f"points = {points}")

            if len(set(points)) == 1:
                d = [p[1] for p in self.points if p[1] in moves_states]
                b = choice(d)
                best = b[-1]
                print(f"best = {best} (choice)")
        # print(f"self.points = {self.points}")


        # print(f"MAX DEPTH = {self.max_depth}")
        # print(f"wins = {self.wins} ..")
        # print(f"points = {self.points}")
        # print(f"best = {best}, points = {max_points}")
        return best

    def best_move(self):
        pass

    def run_simulation(self):
        visited_states = []
        states_copy = self.states[:]
        if len(states_copy) == 0:
            state = self.board
        else:
            state = states_copy[-1]
        player = state.current_player
        player_we_want_to_win = state.current_player
        points_at_end = state.players[player_we_want_to_win.color].score
        expand = True
        turn = 0
        for t in range(self.max_moves):
            self.action.change_board(state)
            legal = self.action.legal_plays()


            play = choice(legal)
            # if t == 0:
            print("____________")
            print(f"t = {t}")
            print(f"play={play}")
            if play[1] == ('end', 0):
                turn +=1
            points_now = state.players[player_we_want_to_win.color].score
            if t == 0:
                print(f"points_now={points_now}")
            state = self.next_state(state, play)
            points_after = state.players[player_we_want_to_win.color].score
            if t == 0:
                print(f"points_after={points_after}")

            states_copy.append(state)

            if expand and self.player_state_in_plays(player, state) is False:
                expand = False
                self.plays[(player.color, tuple(state.history))] = 0
                self.wins[(player.color, tuple(state.history))] = 0
                self.points[(player.color, tuple(state.history))] = 0
                if t > self.max_depth:
                    self.max_depth = t

            self.visited_states_add(visited_states, (player, state))

            player = state.current_player
            winner = state.is_end()
            if points_now < points_after:
                points_at_end += (points_after-points_now) - t*1/self.max_moves
            if type(winner) is int:
                break

        # print("++++++++++++++")
        # print(f"player = {player}, state = {state}")
        # print(visited_states)
        # print("++++++++++++++")
        for player, state in visited_states:
            if self.player_state_in_plays(player_we_want_to_win.color, tuple(state.history)) is False:
                continue
            self.plays[(player_we_want_to_win.color, tuple(state.history))] += 1
            if player_we_want_to_win.color == winner and winner is not False:
                # print(f"winner is {winner} player color is {player.color}")
                # print(f"player won with {player_we_want_to_win.score}")
                self.wins[(player_we_want_to_win.color, tuple(state.history))] += 1
            if self.points[(player_we_want_to_win.color, tuple(state.history))] < points_at_end:
                self.points[(player_we_want_to_win.color, tuple(state.history))] = points_at_end

    def compare_states(self, state1, state2):
        if state1 == state2:
            return True
        return False

    def player_state_in_plays(self, player, state):
        for p, s in self.plays:
            # print(f"p = {p}, player={player}, s = {s}, state = {state}")
            if player == p and state == s:
                # print("same")
                return True
        return False

    def next_state(self, state, play):
        new_state = deepcopy(state)
        self.action.change_board(new_state)
        self.action.ai_move(play)
        return new_state

    def visited_states_add(self, visited_states, t):
        is_in = False
        for i in visited_states:
            if t[0] == i[0] and t[1] == i[1]:
                is_in = True
                break
        if not is_in:
            visited_states.append(t)

