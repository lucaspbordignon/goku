import numba
import numpy as np


# @numba.jit(nopython=True)
def window(iterable, size):
    for i in range(len(iterable) - size + 1):
        yield iterable[i:i + size]

# @numba.jit(nopython=True)
def _array_equal(a, b):
    for x, y in zip(a, b):
        # if x.item() != y.item():
        if x != y:
            return False
    return True

# @numba.jit(nopython=True)
def _sum(iterable, start=0):
    for i in iterable:
        start += i
    return start

# @numba.jit(nopython=True)
def find(pattern, board):
    height, _ = board.shape
    pattern_len = len(pattern)

    def count_row(board):
        return _sum(_array_equal(c, pattern)
                for row in board
                for c in window(row, pattern_len))

    def count_diag(board):
        edge = height - pattern_len
        return _sum(_array_equal(c, pattern)
                for i in range(-edge, edge + 1)
                for c in window(board.diagonal(i), pattern_len))

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
    return find(np.full(2, symbol), board)


def find_triplets(symbol, board):
    return find(np.full(3, symbol), board)


def find_quartets(symbol, board):
    return find(np.full(4, symbol), board)


def find_quintuplets(symbol, board):
    return find(np.full(5, symbol), board)
