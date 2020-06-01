import numpy as np
import piece
import ast
import os
import time
from board import BoardState
from ai import get_best_move
from eval_fn import evaluation_state


def play(size=19, depth=2):
    board_state = BoardState(size, color=piece.WHITE)
    print(board_state)
    play_first = input('[1] First\n[2] Second\n> Your choice: ')
    is_max_state = True
    if int(play_first) == 1:
        is_max_state = False
        while True:
            try:
                move = ast.literal_eval(input("(x, y): "))
                i, j = move
                board_state = board_state.next((i - 1, j - 1))
                print(board_state)
                print(move)
                break
            except:
                continue

    else:
        pass

    while True:
        is_win, color = board_state.check_five_in_a_row()
        if is_win:
            print('[{}] is win'.format(piece.symbols[color]))
            break

        if board_state.is_full():
            print('draw')
            break

        move, value = get_best_move(board_state, depth, is_max_state)
        print(move)
        board_state = board_state.next(move)
        os.system('clear')
        print(board_state)
        i, j = move
        print((i + 1, j + 1), value)

        is_win, color = board_state.check_five_in_a_row()
        if is_win:
            print('[{}] is win'.format(piece.symbols[color]))
            break

        if board_state.is_full():
            print('draw')
            break
        while True:
            try:
                move = ast.literal_eval(input("(x, y): "))
                break
            except:
                continue

        i, j = move
        board_state = board_state.next((i - 1, j - 1))
        os.system('clear')
        print(board_state)
        print(move)


def unmove(state, position):
    state.values[position] = piece.EMPTY


def make_move(state, position, color):
    state.values[position] = color


def defend_policy(state):
    pass


def attack_policy(state):
    pass


def test():
    b = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 1, 0, 1, 1, 0, 0],
         [0, 0, 0, -1, -1, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0]]
    # b = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
    #      [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #      [0, 1, 0, 0, 1, 0, 0, 0, 0],
    #      [0, 0, -1, 0, -1, 0, 0, 0, 0],
    #      [0, 1, 0, 0, -1, 1, -1, 0, 0],
    #      [0, 1, 1, 0, -1, 0, 0, 0, 0],
    #      [0, 0, 0, 0, -1, 0, 0, 0, 0],
    #      [0, 0, 0, 0, 1, 0, 0, 0, 0],
    #      [0, 0, 0, 0, 0, 0, 0, 0, 0]]
    # b = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
    #      [0, 0, -1, 0, 0, -1, 0, 0, 0],
    #      [0, 0, 0, 0, 1, 0, 0, 0, 0],
    #      [0, 0, 0, 0, 1, 0, 0, 0, 0],
    #      [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #      [0, 0, 0, 0, 0, 1, 0, 0, 0],
    #      [0, 0, 0, 0, 1, -1, 0, -1, 0],
    #      [0, 0, 0, 1, 0, 0, 0, 0, 0],
    #      [0, 0, 0, 0, 0, 0, 0, 0, 0]]
    # b = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
    #      [0, 0, 0, 1, 0, 0, 0, 0, 0],
    #      [0, 0, 0, 0, -1, 0, 1, 0, 0],
    #      [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #      [0, 0, 0, 1, 0, 0, -1, 0, 0],
    #      [0, 0, 1, 1, 0, -1, 0, 0, 0],
    #      [0, 0, 0, 1, -1, 0, -1, 0, 0],
    #      [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #      [0, 0, 0, 0, 0, 0, 0, 0, 0]]
    state = BoardState(9, b, color=piece.BLACK)
    state.last_move = (2, 3)
    # state.last_move = (7, 3)
    print(state)
    print(evaluation_state(state, piece.WHITE))
    move, value = get_best_move(state, 2, is_max_state=False)
    state = state.next(move)
    print(state)
    print(evaluation_state(state, piece.BLACK))


if __name__ == "__main__":
    test()
    # play()
