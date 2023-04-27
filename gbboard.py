from copy import deepcopy
import numpy as np
from gbtypes import Player
from typing import Tuple, Optional

COL_NAMES = 'ABCDEFGHJKLMNOP'
BOARD_SIZE = 15
neighbors = [(0, 1), (1, 0), (0, -1), (-1, 0),
             (1, 1), (-1, -1), (1, -1), (-1, 1)]


class Board:
    def __init__(self):
        self._grid = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=np.int_)
        self.surplus = BOARD_SIZE*BOARD_SIZE

    def place_stone(self, point: Tuple, player: Player):
        assert self._grid[point] == 0
        self._grid[point] = player.value
        self.surplus -= 1

    @staticmethod
    def is_on_board(point: Tuple):
        return 0 <= point[0] < BOARD_SIZE and 0 <= point[1] < BOARD_SIZE

    def get_one_line(self, line_shape, index):
        """

        :param line_shape: 0:一; 1:|; 2:╲; 3:╱
        :param index:
        :return:
        """
        if line_shape == 0:
            return self._grid[index]  # r
        elif line_shape == 1:
            return self._grid[:, index]  # c
        elif line_shape == 2:
            return self._grid.diagonal(offset=index)  # c-r
        elif line_shape == 3:
            return np.fliplr(self._grid).diagonal(offset=index)   # BOARD_SIZE-1-c-r
        else:
            raise ValueError("The value of line_shape is [0,1,2,3]")

    @property
    def get_grid(self):
        return self._grid.copy()

    def get_player(self, point: Tuple):
        return Player.value2player(self._grid[point])


class Move:
    def __init__(self, point: Optional[Tuple] = None, is_resign: bool = False):
        assert (point is not None) ^ is_resign
        self.point = point
        self.is_resign = is_resign

    @classmethod
    def play(cls, point: Tuple):
        return Move(point)

    @classmethod
    def resign(cls):
        return Move(is_resign=True)

    def __str__(self):
        if self.is_resign:
            return 'resign'
        return COL_NAMES[self.point[1]]+str(self.point[0]+1)

    def __eq__(self, other: 'Move'):
        if self.is_resign:
            return other.is_resign
        else:
            if other.is_resign:
                return False
            else:
                return self.point == other.point


class GameState:
    def __init__(self, board: Board, next_player: Player, last_move: Optional[Move]):
        self.board = board
        self.next_player = next_player
        self.last_move = last_move
        self.winner: Optional[Player] = None
        # self._possible_moves = []

    @classmethod
    def new_game(cls):
        board = Board()
        return cls(board, Player.black, None)

    def apply_move(self, move: Move):
        if move.is_resign:
            new_board = self.board
            new_state = GameState(new_board, self.next_player.other, move)
        else:
            new_board = deepcopy(self.board)
            new_board.place_stone(move.point, self.next_player)

            new_state = GameState(new_board, self.next_player.other, move)

            # new_state._possible_moves = self._possible_moves.copy()
            # if move in new_state._possible_moves:
            #     new_state._possible_moves.remove(move)
            # for neighbor in neighbors:
            #     neighbor_point = (move.point[0] + neighbor[0], move.point[1] + neighbor[1])
            #     neighbor_move = Move.play(neighbor_point)
            #     if not self.board.is_on_board(neighbor_point):
            #         continue
            #     if neighbor_move not in new_state._possible_moves and new_board.get_player(neighbor_point) is None:
            #         new_state._possible_moves.append(neighbor_move)

        return new_state

    def is_over(self):
        if self.last_move is None:
            return False
        elif self.last_move.is_resign:
            self.winner = self.next_player
            return True

        r, c = self.last_move.point
        horizontal = self.board.get_one_line(0, r)
        result = self._scan_line(horizontal)
        if result == 1:
            self.winner = Player.black
            return True
        elif result == -1:
            self.winner = Player.white
            return True

        vertical = self.board.get_one_line(1, c)
        result = self._scan_line(vertical)
        if result == 1:
            self.winner = Player.black
            return True
        elif result == -1:
            self.winner = Player.white
            return True

        left_diagonal = self.board.get_one_line(2, c-r)
        result = self._scan_line(left_diagonal)
        if result == 1:
            self.winner = Player.black
            return True
        elif result == -1:
            self.winner = Player.white
            return True

        right_diagonal = self.board.get_one_line(3, BOARD_SIZE-1-c-r)
        result = self._scan_line(right_diagonal)
        if result == 1:
            self.winner = Player.black
            return True
        elif result == -1:
            self.winner = Player.white
            return True

        if self.board.surplus == 0:
            return True

        return False

    def _scan_line(self, line: np.ndarray):
        for i in range(line.size-4):
            window = line[i:i+5]
            if np.array_equal(np.ones(5), window):
                return 1
            if np.array_equal(-1*np.ones(5), window):
                return -1
        return 0

    # def legal_moves(self):
    #     moves = []
    #     board = self.board.get_grid
    #     for p in zip(*np.nonzero(board == 0)):
    #         moves.append(Move.play(p))
    #     moves.append(Move.resign())
    #     return moves

    def possible_moves(self, include_resign=False):
        moves = []
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                point = (r, c)
                if self.board.get_player(point) is None:
                    if self.have_any_neighbors(point):
                        moves.append(Move.play(point))
        if include_resign:
            moves.append(Move.resign())
        # np.random.shuffle(moves)
        return moves

    # @property
    # def possible_moves(self):
    #     return self._possible_moves

    def have_any_neighbors(self, point):
        for neighbor in neighbors:
            neighbor_point = (point[0] + neighbor[0], point[1] + neighbor[1])
            if not self.board.is_on_board(neighbor_point):
                continue
            if self.board.get_player(neighbor_point) is not None:
                return True
        return False

    def is_valid_move(self, move: Move):
        if move.is_resign:
            return True
        else:
            return Board.is_on_board(move.point) and self.board.get_player(
                move.point) is None and self.winner is None


if __name__ == '__main__':
    game = GameState.new_game()
    game = game.apply_move(Move.play((7, 7)))
    for m in game.possible_moves():
        print(m)
