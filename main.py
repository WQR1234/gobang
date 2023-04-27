import time

from agent import *
from evaluation import evaluation_fn
from gbboard import Board, GameState, Move
from gbtypes import Player

COL_NAMES = 'ABCDEFGHJKLMNOP'


def print_board(board: Board):
    print('    A   B   C   D   E   F   G   H   J   K   L   M   N   O   P')
    for row in range(1, 16):
        pieces = []
        for col in range(1, 16):
            piece = board.get_player((row-1, col-1))
            if piece == Player.black:
                pieces.append('X')
            elif piece == Player.white:
                pieces.append('O')
            else:
                pieces.append(' ')
        if row < 10:
            print(' %d  %s' % (row, ' | '.join(pieces)))
        else:
            print('%d  %s' % (row, ' | '.join(pieces)))
    print()


def move_from_coords(text):
    if text == '0':
        return Move.resign()
    r = int(text[1:])-1
    c = COL_NAMES.index(text[0])
    return Move.play((r, c))


def main():
    game = GameState.new_game()

    choice1 = input("choice black:(1: human, 2:alpha_beta, 3: mcts)")
    if choice1 == '1':
        player1 = Human()
    elif choice1 == '2':
        player1 = AlphaBetaAgent(3, evaluation_fn)
    else:
        player1 = MCTSAgent(4000, 1.1)

    choice2 = input("choice white:(1: human, 2:robot, 3: mcts)")
    if choice2 == '1':
        player2 = Human()
    elif choice2 == '2':
        player2 = RandomBot()
    else:
        player2 = MCTSAgent(4000, 1.1)

    player = player1

    flag = True

    while not game.is_over():
        print_board(game.board)
        print(game.next_player)
        # print(evaluation(game))

        s = time.time()
        move = player.select_move(game)
        e = time.time()
        print(e-s, 's')

        game = game.apply_move(move)

        flag = not flag
        if flag:
            player = player1
        else:
            player = player2

    print_board(game.board)
    winner = game.winner

    if winner is None:
        print("It's a draw.")
    else:
        print('Winner: ' + str(winner))


if __name__ == '__main__':
    main()


