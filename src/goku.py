import math

import numpy as np

from constants import BOARD_SIZE


def window(iterable, size):
    for i in range(len(iterable) - size + 1):
        yield iterable[i:i + size]


# TODO: Return the position for the next move, not only the heuristic value
def find(length, symbol, board):
    pattern = np.array([symbol] * length)

    def count_row(board):
        return sum(np.array_equal(c, pattern)
                   for row in board
                   for c in window(row, length))

    def count_diag(board):
        return sum(np.array_equal(c, pattern)
                   for i in range(-(BOARD_SIZE - length), (BOARD_SIZE - length) + 1)
                   for c in window(board.diagonal(i), length))

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


def find_doubles(symbol, board):
    return find(2, symbol, board)

def find_triples(symbol, board):
    return find(3, symbol, board)

def find_quartets(symbol, board):
    return find(4, symbol, board)

class Goku:
    """
        Implements the AI agent for the gomoku game. It uses the minimax
    algorithm to find the best option for the next move, using alpha-beta
    pruning
    """

    def next_move(self, board):
        """
            Makes the search and returns the coordinates for the best move
        found. Should be the only function to be called externally.
        """
        pass

    def minimax(self, board, alpha, beta, current_player='G', max_level=3):
        """
            Minimax algorith with alpha-beta prunning. Must return not only the
        node value, but the next movement coordinates.
        """
        # Leaf node
        if max_level == 0:
            return self.heuristic(board)

        if current_player == 'G':
            value = -math.inf
            for next_board, movement in self.all_movement_possibilities(board):
                print('A')
                value = max(value, self.minimax(next_board,
                                                alpha,
                                                beta,
                                                'X',
                                                max_level - 1))
                alpha = max(value, alpha)
                # Cutting off
                if alpha > beta:
                    break
            return value
        else:
            value = math.inf
            for next_board, movement in self.all_movement_possibilities(board):
                value = min(value, self.minimax(next_board,
                                                alpha,
                                                beta,
                                                'G',
                                                max_level - 1))
                alpha = min(value, alpha)
                # Cutting off
                if alpha > beta:
                    break
            return value

    def all_movement_possibilities(self, board):
        for item in np.argwhere(board == '.'):
            yield tuple(item)

    def heuristic(self, board):
        postive_factor = (find_doubles('G', board) +
                          150 * find_triples('G', board) +
                          95 * find_quartets('G', board))
        negative_factor = (find_doubles('X', board) +
                           150 * find_triples('X', board) +
                           95 * find_quartets('X', board))

        return postive_factor - 0.5 * negative_factor
