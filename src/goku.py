import contextlib
import functools
import time
import enum
import logging
import math
import numpy as np
from constants import BOARD_SIZE
from transposition import TranspositionTable


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


def window(iterable, size):
    for i in range(len(iterable) - size + 1):
        yield iterable[i:i + size]


def _find(pattern, board):
    height, _ = board.shape
    pattern_len = len(pattern)
    def count_row(board):
        return sum(np.array_equal(c, pattern)
                for row in board
                for c in window(row, pattern_len))

    def count_diag(board):
        edge = height - pattern_len
        return sum(np.array_equal(c, pattern)
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
    return _find(2, symbol, board)


def find_triplets(symbol, board):
    return _find(3, symbol, board)


def find_quartets(symbol, board):
    return _find(4, symbol, board)


def find_quintuplets(symbol, board):
    return _find(5, symbol, board)


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

    >>> moves = _possible_next_moves(np.full((3, 3), '.'), 'X')
    >>> next(moves, 'X')
    array([['.', '.', '.'],
           ['.', 'X', '.'],
           ['.', '.', '.']], dtype='<U1')
    >>> next(moves, 'X')
    array([['X', '.', '.'],
           ['.', '.', '.'],
           ['.', '.', '.']], dtype='<U1')
    >>> next(moves, 'X')
    array([['.', 'X', '.'],
           ['.', '.', '.'],
           ['.', '.', '.']], dtype='<U1')

    >>> moves = _possible_next_moves(np.full((15, 15), '.'), 'X')
    >>> first, *_, last = moves
    >>> first[6:9, 6:9]
    array([['.', '.', '.'],
           ['.', 'X', '.'],
           ['.', '.', '.']], dtype='<U1')
    >>> last[0:3, 0:3]
    array([['.', '.', '.'],
           ['X', '.', '.'],
           ['.', '.', '.']], dtype='<U1')
    >>> next(moves)
    Traceback (most recent call last):
        ...
    StopIteration
    """
    height, width = board.shape
    assert height == width
    for x, y in _spiral_index(height):
        if board[x, y] == '.':
            move = np.copy(board)
            move[x, y] = player
            yield (x, y), move


LENGTH_FACTOR = 5

def _evaluate(board, player, opponent):

    def find_pattern(pattern):
        return _find(pattern, board)

    def score(player, opponent):
        open_doublet = np.array(['.', player, player, '.'])
        closed_doublet = np.array([opponent, player, player, '.'])

        open_triplet = np.array(['.', player, player, player, '.'])
        closed_triplet = np.array([opponent, player, player, player, '.'])

        open_quadruplet = np.array(['.', player, player, player, player, '.'])
        closed_quadruplet = np.array([opponent, player, player, player, player, '.'])

        quintuplet = np.array([player, player, player, player, player])

        return 10 * find_pattern(open_doublet) + \
                1 * (find_pattern(closed_doublet) + find_pattern(closed_doublet[::-1])) + \
                100 * find_pattern(open_doublet) + \
                10 * (find_pattern(closed_triplet) + find_pattern(closed_triplet[::-1])) + \
                1000 * find_pattern(open_quadruplet) + \
                100 * (find_pattern(closed_quadruplet) + find_pattern(closed_quadruplet[::-1])) + \
                10000 * find_pattern(quintuplet)

    return score(player, opponent) - score(opponent, player)


OPPONENT_MAP = {
        'G': 'X',
        'X': 'G',
        }
def minimax(board, depth, maximizing, player, alpha=-math.inf, beta=math.inf):
    """
        Minimax algorith with alpha-beta prunning. Must return not only the
    node value, but the next movement coordinates.
    """
    best_move = ()
    # Leaf node
    if depth == 0:
        return (_evaluate(board, player, OPPONENT_MAP[player]), ())

    # if current_player == 'G':
    if maximizing:
        value = -math.inf
        for position, state in _possible_next_moves(board, 'G'):
            new_value, _ = minimax(state, depth - 1, False, 'X', alpha, beta)
            if new_value > value:
                value, best_move = new_value, position
            alpha = max(value, alpha)

            # Cutting off
            if beta <= alpha:
                break
        return value, best_move
    else:
        value = math.inf
        for position, state in _possible_next_moves(board, 'X'):
            new_value, _ = minimax(state, depth - 1, True, 'G', alpha, beta)
            if new_value < value:
                value, best_move = new_value, position
            beta = min(value, beta)

            # Cutting off
            if beta <= alpha:
                break
        return value, best_move


def _next_move(board, max_level=1):
    value, position = minimax(board, max_level, True, 'G')
    return position


class Goku:
    """
        Implements the AI agent for the gomoku game. It uses the minimax
    algorithm to find the best option for the next move, using alpha-beta
    pruning
    """

    def __init__(self):
        self._transposition_table = TranspositionTable()

    @timed
    def next_move(self, board, max_level=1):
        """
            Makes the search and returns the coordinates for the best move
        found. Should be the only function to be called externally.
        """
        return _next_move(board, max_level)
        # value, position = self.minimax(board, max_level=max_level)
        # return position

    def all_movement_possibilities(self, board):
        # Makes : spiral, starting from the center
        repeating_positions = False
        central_index = BOARD_SIZE // 2
        current_position = np.array([central_index, central_index])
        current_direction = Direction.RIGHT
        change_move_count = 1
        current_move_count = 1
        local_count = 2

        while not repeating_positions:
            if board[current_position] != '.':
                current_move_count -= 1
            else:
                yield current_position
                current_move_count -= 1

            x, y = current_position
            current_position += DIRECTION_DELTA[current_direction]

            if BOARD_SIZE in current_position:
                repeating_positions = True

            if current_move_count == 0:
                local_count -= 1
                if local_count == 0:
                    local_count = 2
                    change_move_count += 1

                current_move_count = change_move_count

                current_direction = (current_direction + 1) % len(Direction)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
