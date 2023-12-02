
from gbtypes import Player


class Board:
    def __init__(self):
        self.grid = [0] * 225
        self.manual = []
        self.step_num = 0
        self.winner = Player.Empty
        # self.surplus = BOARD_SIZE*BOARD_SIZE

    def is_valid_move(self, point: int):
        return self.grid[point] == 0

    def place_stone(self, point: int, player: Player):
        assert self.grid[point] == 0
        self.grid[point] = player.value
        self.step_num += 1
        self.manual.append(point)
        self.judge_winner()
        # self.surplus -= 1

    # @staticmethod
    # def is_on_board(point: Tuple):
    #     return 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE

    def retract(self):
        last_point = self.manual.pop()
        self.step_num -= 1
        self.grid[last_point] = 0
        self.winner = Player.Empty
        return last_point

    def get_one_line(self, point: int, line_shape) -> str:
        """

        :param line_shape: 0:一; 1:|; 2:╲; 3:╱
        :param point:
        :return:
        """
        r, c = point//15, point % 15
        if line_shape == 0:
            return "".join(map(lambda x: str(x), self.grid[r * 15:r * 15 + 15]))  # r

        elif line_shape == 1:
            return "".join(map(lambda x: str(self.grid[c + 15 * x]), range(15)))  # c

        elif line_shape == 2:
            if c >= r:
                return "".join(map(lambda x: str(self.grid[-15 * (c - r) + 16 * x]), range(c - r, 15)))  # c-r
            else:
                return "".join(map(lambda x: str(self.grid[-15 * (c - r) + 16 * x]), range(15 + c - r)))

        elif line_shape == 3:
            if r + c <= 14:
                return "".join(map(lambda x: str(self.grid[14 * x + r + c]), range(r + c + 1)))   # BOARD_SIZE-1-c-r
            else:
                return "".join(map(lambda x: str(self.grid[14 * x + r + c]), range(r + c - 14, 15)))

        else:
            raise ValueError("The value of line_shape is [0,1,2,3]")

    def judge_winner(self):
        last_point = self.manual[-1]
        win_shape = "11111" if self.step_num%2 else "22222"
        for i in range(4):
            line = self.get_one_line(last_point, i)
            if win_shape in line:
                self.winner = Player.Black if self.step_num%2 else Player.White
                break

    # @property
    # def get_grid(self):
    #     return self._grid.copy()

    def get_player(self, point: int):
        return self.grid[point]

    # def __deepcopy__(self, memodict={}):
    #     board_copy = Board()
    #     board_copy._grid = self._grid.copy()
    #     board_copy.surplus = self.surplus
    #     return board_copy


# class Move:
#     def __init__(self, point: Optional[Tuple] = None, is_resign: bool = False):
#         assert (point is not None) ^ is_resign
#         self.point = point
#         self.is_resign = is_resign
#
#     @classmethod
#     def play(cls, point: Tuple):
#         return Move(point)
#
#     @classmethod
#     def resign(cls):
#         return Move(is_resign=True)
#
#     def __str__(self):
#         if self.is_resign:
#             return 'resign'
#         return COL_NAMES[self.c]+str(self.r+1)
#
#     def __eq__(self, other: 'Move'):
#         if self.is_resign:
#             return other.is_resign
#         else:
#             if other.is_resign:
#                 return False
#             else:
#                 return self.point == other.point
#
#
# class GameState:
#     def __init__(self, board: Board, next_player: Player, last_move: Optional[Move]):
#         self.board = board
#         self.next_player = next_player
#         self.last_move = last_move
#         self.winner: Optional[Player] = None
#         # self._possible_moves = []
#
#     @classmethod
#     def new_game(cls):
#         board = Board()
#         return cls(board, Player.black, None)
#
#     def apply_move(self, move: Move, copy=True):
#         if move.is_resign:
#             new_board = self.board
#             new_state = GameState(new_board, self.next_player.other, move)
#         else:
#             if copy:
#                 new_board = deepcopy(self.board)
#             else:
#                 new_board = self.board
#             new_board.place_stone(move.point, self.next_player)
#
#             new_state = GameState(new_board, self.next_player.other, move)
#
#         return new_state
#
#     def is_over(self):
#         if self.last_move is None:
#             return False
#         elif self.last_move.is_resign:
#             self.winner = self.next_player
#             return True
#
#         for i in range(4):
#             line = self.board.get_one_line(i, self.last_move.point)
#             result = self._scan_line(line)
#             if result == 1:
#                 self.winner = Player.black
#                 return True
#             elif result == -1:
#                 self.winner = Player.white
#                 return True
#
#         if self.board.surplus == 0:
#             return True
#
#         return False
#
#     @staticmethod
#     def _scan_line(line: List):
#         for i in range(len(line)-4):
#             window = line[i:i+5]
#             if window == [1, 1, 1, 1, 1]:
#                 return 1
#             if window == [-1, -1, -1, -1, -1]:
#                 return -1
#         return 0
#
#     # def legal_moves(self):
#     #     moves = []
#     #     board = self.board.get_grid
#     #     for p in zip(*np.nonzero(board == 0)):
#     #         moves.append(Move.play(p))
#     #     moves.append(Move.resign())
#     #     return moves
#
#     def possible_moves(self, include_resign=False):
#         moves = []
#         for r in range(BOARD_SIZE):
#             for c in range(BOARD_SIZE):
#                 point = (r, c)
#                 if self.board.get_player(point) is None:
#                     if self.have_any_neighbors(point):
#                         moves.append(Move.play(point))
#         if include_resign:
#             moves.append(Move.resign())
#         # np.random.shuffle(moves)
#         return moves
#
#     # @property
#     # def possible_moves(self):
#     #     return self._possible_moves
#
#     def have_any_neighbors(self, point):
#         for neighbor in neighbors:
#             neighbor_point = (r + neighbor[0], c + neighbor[1])
#             if not self.board.is_on_board(neighbor_point):
#                 continue
#             if self.board.get_player(neighbor_point) is not None:
#                 return True
#         return False
#
#     def is_valid_move(self, move: Move):
#         if move.is_resign:
#             return True
#         else:
#             return Board.is_on_board(move.point) and self.board.get_player(
#                 move.point) is None and self.winner is None


# if __name__ == '__main__':
#     game = GameState.new_game()
#     game = game.apply_move(Move.play((7, 7)))
#     for m in game.possible_moves():
#         print(m)

if __name__ == '__main__':
    game = Board()
    p = 14
    print(len(game.get_one_line(p, 0)))
    print(len(game.get_one_line(p, 1)))
    print(len(game.get_one_line(p, 2)))
    print(len(game.get_one_line(p, 3)))
