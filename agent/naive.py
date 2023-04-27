import numpy as np

from agent.base import Agent
from gbboard import Move, GameState, BOARD_SIZE

neighbors = [(0, 1), (1, 0), (0, -1), (-1, 0),
             (1, 1), (-1, -1), (1, -1), (-1, 1)]


class RandomBot(Agent):
    def __init__(self):
        Agent.__init__(self)
        self._points_cache = []
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                self._points_cache.append((r, c))

    def select_move(self, game_state: GameState):
        if game_state.board.surplus == BOARD_SIZE*BOARD_SIZE:
            return Move.play((BOARD_SIZE//2, BOARD_SIZE//2))

        idx = np.arange(len(self._points_cache))
        np.random.shuffle(idx)

        for i in idx:
            p = self._points_cache[i]
            if game_state.board.get_player(p) is None:
                if game_state.have_any_neighbors(p):
                    return Move.play(p)

    # def have_any_neighbors(self, point, game_state: GameState):
    #     for neighbor in neighbors:
    #         neighbor_point = (point[0] + neighbor[0], point[1] + neighbor[1])
    #         if not game_state.board.is_on_board(neighbor_point):
    #             continue
    #         if game_state.board.get_player(neighbor_point) is not None:
    #             return True
    #     return False

