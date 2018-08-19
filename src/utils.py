import numpy as np
import regex as re
from constants import DIRECTION_CHANGE_ENUM
from constants import BOARD_SIZE


def spiral_new_direction(current):
    return DIRECTION_CHANGE_ENUM[current]


def sum_tuples(first, second):
    return tuple(np.sum((first, second), axis=0))


def find(symbol, pattern, board):
    """
        Find all the occurrences of a given symbol, 'pattern' times in
    sequence for the given board. Searches for rows, columns, diagonals
    and inverted diagonals
    """
    def count_row(board, start=0):
        for row in board:
            row_string = ''.join(row)
            start += len(re.findall(r'[' + symbol + r']{' + str(pattern) + '}',
                         row_string,
                         overlapped=True))
        return start

    def count_diag(board, start=0):
        index = - (BOARD_SIZE + 1)
        while index < BOARD_SIZE:
            diag_string = ''.join(board.diagonal(index))
            start += len(re.findall(r'[' + symbol + r']{' + str(pattern) + '}',
                         diag_string,
                         overlapped=True))
            index += 1
        return start

    return (
        # Search for the rows
        count_row(board) +

        # Search for the columns
        count_row(np.transpose(board)) +

        # Search for the first diagonal direction with at least length elements
        count_diag(board) +

        # Search for the other direction
        count_diag(np.fliplr(board))
    )


def find_doublets(symbol, board):
    return find(symbol, 2, board)


def find_triplets(symbol, board):
    return find(symbol, 3, board)


def find_quartets(symbol, board):
    return find(symbol, 4, board)
