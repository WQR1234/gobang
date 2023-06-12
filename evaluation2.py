from typing import List

from gbboard import GameState, BOARD_SIZE
from gbtypes import Player

ld_search_lst = [(0, 0), (1, 0), (0, 1), (2, 0), (0, 2), (3, 0), (0, 3), (4, 0), (0, 4), (5, 0), (0, 5), (6, 0), (0, 6),
                 (7, 0), (0, 7), (8, 0), (0, 8), (9, 0), (0, 9), (10, 0), (0, 10)]

rd_search_lst = [(0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (0, 9), (0, 10), (0, 11), (0, 12), (0, 13), (0, 14), (1, 14),
                 (2, 14), (3, 14), (4, 14), (5, 14), (6, 14), (7, 14), (8, 14), (9, 14), (10, 14)]

offensive_score_table = {
    (0, 1, 1, 1, 1): 900,
    (1, 0, 1, 1, 1): 900,
    (1, 1, 0, 1, 1): 900,
    (1, 1, 1, 0, 1): 900,
    (1, 1, 1, 1, 0): 900,
    (0, 1, 1, 1, 0): 99,
    (0, 0, 1, 1, 0): 9,
    (0, 1, 1, 0, 0): 9
}

defensive_score_table = {
    (0, 1, 1, 1, 1): 190,
    (1, 0, 1, 1, 1): 190,
    (1, 1, 0, 1, 1): 190,
    (1, 1, 1, 0, 1): 190,
    (1, 1, 1, 1, 0): 190,
    (0, 1, 1, 1, 0): 29
}


def evaluation_fn(game_state: GameState):
    next_player = game_state.next_player
    total_score = 0
    for r in range(BOARD_SIZE):
        horizontal = game_state.board.get_one_line(0, (r, 0))
        total_score += evaluate_one_line(horizontal, next_player)

    for c in range(BOARD_SIZE):
        vertical = game_state.board.get_one_line(1, (0, c))
        total_score += evaluate_one_line(vertical, next_player)

    for i in ld_search_lst:
        left_diagonal = game_state.board.get_one_line(2, i)
        total_score += evaluate_one_line(left_diagonal, next_player)

    for j in rd_search_lst:
        right_diagonal = game_state.board.get_one_line(3, j)
        total_score += evaluate_one_line(right_diagonal, next_player)

    return total_score


def evaluate_one_line(line: List, next_player: Player):
    if line.count(0) >= len(line) - 3:
        return 0
    total_score = 0
    window_size = 5
    num = next_player.value
    for i in range(len(line)-window_size+1):
        my_window = list(map(lambda x: num*line[x], range(i, i+window_size)))

        opponent_window = list(map(lambda x: -num*line[x], range(i, i+window_size)))
        my_score = offensive_score_table.get(tuple(my_window), 0)
        opponent_score = defensive_score_table.get(tuple(opponent_window), 0)
        total_score = total_score + my_score - opponent_score

    return total_score


if __name__ == '__main__':
    a = [0, 1, 1, 1, 1, -1, -1, -1, 0, -1, -1]
    print(evaluate_one_line(a, Player.black))
