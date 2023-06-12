from copy import deepcopy

from gbtypes import Player
from typing import Tuple, Optional, List

COL_NAMES = 'ABCDEFGHJKLMNOP'
BOARD_SIZE = 15
neighbors = [(0, 1), (1, 0), (0, -1), (-1, 0),
             (1, 1), (-1, -1), (1, -1), (-1, 1)]


class Board:
    def __init__(self):
        self._grid = [0]*225
        self.surplus = BOARD_SIZE*BOARD_SIZE

    def place_stone(self, point: Tuple, player: Player):
        index = point[0]*BOARD_SIZE+point[1]
        assert self._grid[index] == 0
        self._grid[index] = player.value
        self.surplus -= 1

    @staticmethod
    def is_on_board(point: Tuple):
        return 0 <= point[0] < BOARD_SIZE and 0 <= point[1] < BOARD_SIZE

    def get_one_line(self, line_shape, point: Tuple[int]):
        """

        :param line_shape: 0:一; 1:|; 2:╲; 3:╱
        :param index:
        :return:
        """
        if line_shape == 0:
            return self._grid[point[0]*BOARD_SIZE:point[0]*BOARD_SIZE+BOARD_SIZE]  # r

        elif line_shape == 1:
            return list(map(lambda x: self._grid[point[1]+BOARD_SIZE*x], range(BOARD_SIZE)))  # c

        elif line_shape == 2:
            if point[1] >= point[0]:
                return list(map(lambda x: self._grid[-15 * (point[1] - point[0]) + 16 * x], range(point[1] - point[0], 15)))  # c-r
            else:
                return list(
                    map(lambda x: self._grid[-15 * (point[1] - point[0]) + 16 * x], range(15 + point[1] - point[0])))

        elif line_shape == 3:
            if point[0] + point[1] <= 14:
                return list(map(lambda x: self._grid[14 * x + point[0] + point[1]], range(point[0] + point[1] + 1)))   # BOARD_SIZE-1-c-r
            else:
                return list(map(lambda x: self._grid[14 * x + point[0] + point[1]], range(point[0] + point[1]-14, 15)))

        else:
            raise ValueError("The value of line_shape is [0,1,2,3]")

    @property
    def get_grid(self):
        return self._grid.copy()

    def get_player(self, point: Tuple):
        return Player.value2player(self._grid[point[0]*BOARD_SIZE+point[1]])

    def __deepcopy__(self, memodict={}):
        board_copy = Board()
        board_copy._grid = self._grid.copy()
        board_copy.surplus = self.surplus
        return board_copy


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

    def apply_move(self, move: Move, copy=True):
        if move.is_resign:
            new_board = self.board
            new_state = GameState(new_board, self.next_player.other, move)
        else:
            if copy:
                new_board = deepcopy(self.board)
            else:
                new_board = self.board
            new_board.place_stone(move.point, self.next_player)

            new_state = GameState(new_board, self.next_player.other, move)

        return new_state

    def is_over(self):
        if self.last_move is None:
            return False
        elif self.last_move.is_resign:
            self.winner = self.next_player
            return True

        for i in range(4):
            line = self.board.get_one_line(i, self.last_move.point)
            result = self._scan_line(line)
            if result == 1:
                self.winner = Player.black
                return True
            elif result == -1:
                self.winner = Player.white
                return True

        if self.board.surplus == 0:
            return True

        return False

    @staticmethod
    def _scan_line(line: List):
        for i in range(len(line)-4):
            window = line[i:i+5]
            if window == [1, 1, 1, 1, 1]:
                return 1
            if window == [-1, -1, -1, -1, -1]:
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
