import contextlib
import functools
import time
import enum
import logging
import math
import numpy as np
from typing import Tuple
from constants import BOARD_SIZE, Player
from transposition import TranspositionTable
import utils


@contextlib.contextmanager
def _timed():
    start = time.time()
    yield
    end = time.time()
    logging.info(f'Execution time: {end - start}s')

def timed(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        with _timed():
            return fn(*args, **kwargs)
    return wrapper


def find_all_pieces(symbol, board):
    return len(np.where(board == symbol))


class Direction(enum.IntEnum):
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3


def _spiral_index(side):
    """Generate spiral indexes for square matrixes of side-length `side`.

    >>> i = _spiral_index(1)
    >>> next(i)
    array([0, 0])
    >>> next(i)
    Traceback (most recent call last):
        ...
    StopIteration

    >>> i = _spiral_index(3)
    >>> next(i)
    array([1, 1])
    >>> next(i)
    array([0, 0])
    >>> next(i)
    array([0, 1])
    >>> next(i)
    array([0, 2])
    >>> next(i)
    array([1, 2])
    >>> next(i)
    array([2, 2])
    >>> next(i)
    array([2, 1])
    >>> next(i)
    array([2, 0])
    >>> next(i)
    array([1, 0])
    >>> next(i)
    Traceback (most recent call last):
        ...
    StopIteration
    """
    DELTA = [
        np.array([0, 1]),
        np.array([1, 0]),
        np.array([0, -1]),
        np.array([-1, 0]),
        ]

    center = np.array([side // 2, side // 2])

    yield center
    for layer in range(side // 2 + 1):
        # start on top-left corner, spirals around center clockwise
        position = center - np.array([layer, layer])
        for direction in Direction:
            for _ in range(layer * 2):
                yield position
                position += DELTA[direction]


def _possible_next_moves(board, player):
    """Generate next possible movement for board and player

    >>> moves = _possible_next_moves(np.full((3, 3), 0), 0)
    >>> next(moves, 0)
    array([[0, 0, 0],
           [0, 0, 0],
           [0, 0, 0]], dtype='<U1')
    >>> next(moves, 0)
    array([[0, 0, 0],
           [0, 0, 0],
           [0, 0, 0]], dtype='<U1')
    >>> next(moves, 0)
    array([[0, 0, 0],
           [0, 0, 0],
           [0, 0, 0]], dtype='<U1')

    >>> moves = _possible_next_moves(np.full((15, 15), 0), 0)
    >>> first, *_, last = moves
    >>> first[6:9, 6:9]
    array([[0, 0, 0],
           [0, 0, 0],
           [0, 0, 0]], dtype='<U1')
    >>> last[0:3, 0:3]
    array([[0, 0, 0],
           [0, 0, 0],
           [0, 0, 0]], dtype='<U1')
    >>> next(moves)
    Traceback (most recent call last):
        ...
    StopIteration
    """
    height, width = board.shape
    assert height == width
    for x, y in _spiral_index(height):
        if board[x, y] == None:
            move = np.copy(board)
            move[x, y] = player
            yield (x, y), move


def _evaluate(board, player, opponent):

    def find_pattern(pattern):
        return utils.find(pattern, board)

    def score(player, opponent):
        open_doublet = np.array([None, player, player, None])
        closed_doublet = np.array([opponent, player, player, None])

        open_triplet = np.array([None, player, player, player, None])
        closed_triplet = np.array([opponent, player, player, player, None])

        open_quadruplet = np.array([None, player, player, player, player, None])
        closed_quadruplet = np.array([opponent, player, player, player, player, None])

        quintuplet = np.array([player, player, player, player, player])

        return 10 * find_pattern(open_doublet) + \
                1 * (find_pattern(closed_doublet) + find_pattern(closed_doublet[::-1])) + \
                100 * find_pattern(open_doublet) + \
                10 * (find_pattern(closed_triplet) + find_pattern(closed_triplet[::-1])) + \
                1000 * find_pattern(open_quadruplet) + \
                100 * (find_pattern(closed_quadruplet) + find_pattern(closed_quadruplet[::-1])) + \
                10000 * find_pattern(quintuplet)

    return score(player, opponent) - 2 * score(opponent, player)


def minimax(board, depth, maximizing, player, opponent, alpha=-math.inf, beta=math.inf):
    """
        Minimax algorith with alpha-beta prunning. Must return not only the
    node value, but the next movement coordinates.
    """
    # Leaf node
    if depth == 0:
        return (_evaluate(board, player, opponent), ())

    if maximizing:
        best_move, best_value = tuple(), -math.inf
        for position, state in _possible_next_moves(board, player):
            new_value, _ = minimax(state, depth - 1, False, player, opponent, alpha, beta)

            if new_value > best_value:
                best_move, best_value = position, new_value

            alpha = max(alpha, best_value)

            # Cutting off
            if beta <= alpha:
                break

        return best_value, best_move
    else:
        best_move, best_value = tuple(), math.inf
        for position, state in _possible_next_moves(board, opponent):
            new_value, _ = minimax(state, depth - 1, True, player, opponent, alpha, beta)

            if new_value > best_value:
                best_move, best_value = position, new_value

            beta = min(beta, best_value)

            # Cutting off
            if beta <= alpha:
                break

        return best_value, best_move


def _next_move(board, depth, index, opponent_index):
    value, position = minimax(board, depth, 1, True, index, opponent_index)
    return position


class Goku:
    """
        Implements the AI agent for the gomoku game. It uses the minimax
    algorithm to find the best option for the next move, using alpha-beta
    pruning
    """

    def __init__(self, index, opponent_index):
        self._transposition_table = TranspositionTable()
        self.index = index
        self.opponent_index = opponent_index

    @timed
    def next_move(self, board, max_level=3):
        """
            Makes the search and returns the coordinates for the best move
        found. Should be the only function to be called externally.
        """
        return _next_move(board, max_level, self.index, self.opponent_index)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
