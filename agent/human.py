from agent.base import Agent
from gbboard import Move


class Human(Agent):
    COL_NAMES = 'ABCDEFGHJKLMNOP'

    def _move_from_coords(self, r_str, c_str):
        r = int(r_str) - 1
        c = Human.COL_NAMES.index(c_str)

        return Move.play((r, c))

    def select_move(self, game_state):
        while True:
            human_move = input('--- ')
            if human_move == '0':
                return Move.resign()
            r_str, c_str = human_move[1:], human_move[0]

            if r_str.isdigit() and c_str in Human.COL_NAMES:
                move = self._move_from_coords(r_str, c_str)
                if game_state.is_valid_move(move):
                    break
        return move
