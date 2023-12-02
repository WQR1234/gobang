import time

from agent import *
# from evaluation2 import evaluation_fn
from gbboard2 import Board
from gbtypes import Player

COL_NAMES = 'ABCDEFGHJKLMNOP'


def print_board(board: Board):
    print('    A   B   C   D   E   F   G   H   J   K   L   M   N   O   P')
    for row in range(1, 16):
        pieces = []
        for col in range(1, 16):
            piece = board.get_player((row-1)*15+col-1)
            if piece == 1:
                pieces.append('X')
            elif piece == 2:
                pieces.append('O')
            else:
                pieces.append(' ')
        if row < 10:
            print(' %d  %s' % (row, ' | '.join(pieces)))
        else:
            print('%d  %s' % (row, ' | '.join(pieces)))
    print()


def move_from_coords(text):
    r = int(text[1:])-1
    c = COL_NAMES.index(text[0])
    return r*15+c


def main():
    game = Board()

    black_id = int(input("choice black:(1: human, 2:robot)"))
    white_id = int(input("choice white:(1: human, 2:robot)"))

    player = Player.Black
    robot = Agent()
    robot.game = game


    while game.winner == Player.Empty:
        print_board(game)
        print(player)
        # print(evaluation(game))

        s = time.time()
        if player == Player.Black:
            if black_id == 1:
                move = move_from_coords(input('black next move:'))
            else:
                if game.step_num == 0:
                    move = 112
                else:
                    move = robot.choice_move()
        else:
            if white_id == 1:
                move = move_from_coords(input('white next move:'))
            else:
                move = robot.choice_move()
        e = time.time()
        print(e-s, 's')

        game.place_stone(move, player)

        player = player.other

    print_board(game)
    winner = game.winner

    if winner is None:
        print("It's a draw.")
    else:
        print('Winner: ' + str(winner))


if __name__ == '__main__':
    main()


