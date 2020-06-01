import piece
import numpy as np
from eval_fn import evaluation_state


def get_best_move(state, depth, is_max_state):
    values = state.values
    best_value = is_max_state and -9999 or 9999
    best_move = (-1, -1)
    pieces = len(values[values != piece.EMPTY])

    if pieces == 0:
        return first_move(state)
    if pieces == 1:
        return second_move(state)

    top_moves = get_top_moves(state, 10, is_max_state)

    for move_n_value in top_moves:
        move = move_n_value[0]
        value = minimax(state.next(move),
                        -10e5,
                        10e5,
                        depth - 1,
                        not is_max_state)

        if ((is_max_state and value > best_value)
                or (not is_max_state and value < best_value)):
            best_value = value
            best_move = move
            # print(best_move, best_value)

    if best_move[0] == -1 and best_move[1] == -1:
        return top_moves[0]

    return best_move, best_value


def get_top_moves(state, n, is_max_state):
    color = state.color
    top_moves = []

    for move in state.legal_moves():
        evaluation = evaluation_state(state.next(move), color)
        top_moves.append((move, evaluation))
    return sorted(top_moves, key=lambda x: x[1], reverse=is_max_state)[:n]


def minimax(state, alpha, beta, depth, is_max_state):
    if depth == 0 or state.is_terminal():
        return evaluation_state(state, -state.color)

    if is_max_state:
        value = -9999
        for move in state.legal_moves():
            value = max(
                value,
                minimax(state.next(move), alpha, beta, depth - 1, False)
            )
            alpha = max(value, alpha)
            if alpha >= beta:
                break
        return value
    else:
        value = 9999
        for move in state.legal_moves():
            value = min(
                value,
                minimax(state.next(move), alpha, beta, depth - 1, True)
            )
            beta = min(value, beta)
            if alpha >= beta:
                break
        return value


def first_move(state):
    x = state.size // 2
    return np.random.choice((x - 1, x, x + 1), 2), 1


def second_move(state):
    i, j = state.last_move
    size = state.size
    i2 = i <= size // 2 and 1 or -1
    j2 = j <= size // 2 and 1 or -1
    return (i + i2, j + j2), 2
