import numpy as np

from gbboard import GameState, BOARD_SIZE
from gbtypes import Player


offensive_score_table = {
    (0, 1, 1, 1, 1): 900,
    (1, 0, 1, 1, 1): 900,
    (1, 1, 0, 1, 1): 900,
    (1, 1, 1, 0, 1): 900,
    (1, 1, 1, 1, 0): 900,
    (0, 1, 1, 1, 0): 99,
    # (-1, 1, 1, 1, 0): 20,
    # (0, 1, 1, 1, -1): 20
}

defensive_score_table = {
    (0, 1, 1, 1, 1): 90,
    (1, 0, 1, 1, 1): 90,
    (1, 1, 0, 1, 1): 90,
    (1, 1, 1, 0, 1): 90,
    (1, 1, 1, 1, 0): 90,
    (0, 1, 1, 1, 0): 9
}


def evaluation_fn(game_state: GameState):
    next_player = game_state.next_player
    total_score = 0
    for r in range(BOARD_SIZE):
        horizontal = game_state.board.get_one_line(0, r)
        total_score += evaluate_one_line(horizontal, next_player)

    for c in range(BOARD_SIZE):
        vertical = game_state.board.get_one_line(1, c)
        total_score += evaluate_one_line(vertical, next_player)

    for i in range(-BOARD_SIZE+5, BOARD_SIZE-4):
        left_diagonal = game_state.board.get_one_line(2, i)
        total_score += evaluate_one_line(left_diagonal, next_player)

    for j in range(-BOARD_SIZE+5, BOARD_SIZE-4):
        right_diagonal = game_state.board.get_one_line(3, j)
        total_score += evaluate_one_line(right_diagonal, next_player)

    return total_score


def evaluate_one_line(line: np.ndarray, next_player: Player):
    if np.count_nonzero(line) < 3:
        return 0
    total_score = 0
    window_size = 5
    num = next_player.value
    for i in range(line.size-window_size+1):
        my_window = num*line[i:i+window_size]
        opponent_window = -my_window
        my_score = offensive_score_table.get(tuple(my_window), 0)
        opponent_score = defensive_score_table.get(tuple(opponent_window), 0)
        total_score = total_score + my_score - opponent_score

    return total_score


if __name__ == '__main__':
    a = np.array([0, 1, 1, 1, 1, -1, -1, -1, 0, -1, -1])
    print(evaluate_one_line(a, Player.black))
