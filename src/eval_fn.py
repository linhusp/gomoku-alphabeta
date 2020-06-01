import numpy as np
import piece


def evaluation_state(state, current_color):
    return evaluate_color(state, piece.BLACK, current_color) + \
        evaluate_color(state, piece.WHITE, current_color)


def evaluate_color(state, color, current_color):
    values = state.values
    size = state.size
    current = color == current_color
    evaluation = 0

    # evaluate rows and cols
    for i in range(size):
        evaluation += evaluate_line(values[i, :], color, current)
        evaluation += evaluate_line(values[:, i], color, current)

    # evaluate diags
    for i in range(-size + 5, size - 4):
        evaluation += evaluate_line(np.diag(values, k=i),
                                    color,
                                    current)
        evaluation += evaluate_line(np.diag(np.fliplr(values), k=i),
                                    color,
                                    current)

    return evaluation * color


def evaluate_line(line, color, current):
    evaluation = 0
    size = len(line)
    # consecutive
    consec = 0
    block_count = 2
    empty = False

    for i in range(len(line)):
        value = line[i]
        if value == color:
            consec += 1
        elif value == piece.EMPTY and consec > 0:
            if not empty and i < size - 1 and line[i + 1] == color:
                empty = True
            else:
                evaluation += calc(consec, block_count - 1, current, empty)
                consec = 0
                block_count = 1
                empty = False
        elif value == piece.EMPTY:
            block_count = 1
        elif consec > 0:
            evaluation += calc(consec, block_count, current)
            consec = 0
            block_count = 2
        else:
            block_count = 2

    if consec > 0:
        evaluation += calc(consec, block_count, current)

    return evaluation


def calc(consec, block_count, is_current, has_empty_space=False):
    if block_count == 2 and consec < 5:
        return 0

    if consec >= 5:
        if has_empty_space:
            return 8000
        return 100000

    consec_score = (2, 5, 1000, 10000)
    # 3: 0.05
    block_count_score = (0.5, 0.6, 0.01, 0.25)
    not_current_score = (1, 1, 0.2, 0.15)
    empty_space_score = (1, 1.2, 0.9, 0.4)

    consec_idx = consec - 1
    value = consec_score[consec_idx]
    if block_count == 1:
        value *= block_count_score[consec_idx]
    if not is_current:
        value *= not_current_score[consec_idx]
    if has_empty_space:
        value *= empty_space_score[consec_idx]
    return int(value)
