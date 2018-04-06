import math
import numpy as np
from constants import BOARD_SIZE
from transposition import TranspositionTable


def window(iterable, size):
    for i in range(len(iterable) - size + 1):
        yield iterable[i:i + size]


def find(length, symbol, board):
    pattern = np.array([symbol] * length)

    def count_row(board):
        return sum(np.array_equal(c, pattern)
                   for row in board
                   for c in window(row, length))

    def count_diag(board):
        edge = BOARD_SIZE - length
        return sum(np.array_equal(c, pattern)
                   for i in range(-edge, edge + 1)
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


def find_all_pieces(symbol, board):
    return len(np.where(board == symbol))


class Goku:
    """
        Implements the AI agent for the gomoku game. It uses the minimax
    algorithm to find the best option for the next move, using alpha-beta
    pruning
    """

    def __init__(self):
        self._transposition_table = TranspositionTable()

    def next_move(self, board, max_level=3):
        """
            Makes the search and returns the coordinates for the best move
        found. Should be the only function to be called externally.
        """
        value, position = self.minimax(board, max_level=max_level)
        return position

    def minimax(self, board,
                alpha=-math.inf,
                beta=math.inf,
                current_player='G',
                max_level=3):
        """
            Minimax algorith with alpha-beta prunning. Must return not only the
        node value, but the next movement coordinates.
        """
        best_movement = ()

        # Leaf node
        if max_level == 0:
            return (self.heuristic(board), ())

        if current_player == 'G':
            value = -math.inf
            for movement in self.all_movement_possibilities(board):
                next_board = np.copy(board)
                next_board[movement] = current_player
                hash_key = self._transposition_table.hash_key(next_board)
                if self._transposition_table.contains(hash_key):
                    minimax = self._transposition_table.value(hash_key)
                else:
                    minimax, _ = self.minimax(next_board,
                                              alpha,
                                              beta,
                                              'X',
                                              max_level - 1)
                    self._transposition_table.insert(hash_key, minimax)
                if minimax > value:
                    value = minimax
                    best_movement = movement
                alpha = max(value, alpha)

                # Cutting off
                if beta <= alpha:
                    break
            return value, best_movement
        else:
            value = math.inf
            for movement in self.all_movement_possibilities(board):
                next_board = np.copy(board)
                next_board[movement] = current_player
                hash_key = self._transposition_table.hash_key(next_board)
                if self._transposition_table.contains(hash_key):
                    minimax = self._transposition_table.value(hash_key)
                else:
                    minimax, _ = self.minimax(next_board,
                                              beta,
                                              alpha,
                                              'G',
                                              max_level - 1)
                    self._transposition_table.insert(hash_key, minimax)
                if minimax < value:
                    value = minimax
                    best_movement = movement
                beta = min(value, beta)

                # Cutting off
                if beta <= alpha:
                    break
            return value, best_movement

    def all_movement_possibilities(self, board):
        # Makes a spiral, starting from the center
        repeating_positions = False
        central_index = BOARD_SIZE // 2
        current_position = (central_index, central_index)
        current_direction = 'RIGHT'
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
            if current_direction == 'LEFT':
                current_position = (x - 1, y)
            elif current_direction == 'RIGHT':
                current_position = (x + 1, y)
            elif current_direction == 'UP':
                current_position = (x, y - 1)
            elif current_direction == 'DOWN':
                current_position = (x, y + 1)

            if BOARD_SIZE in current_position:
                repeating_positions = True

            if current_move_count == 0:
                local_count -= 1
                if local_count == 0:
                    local_count = 2
                    change_move_count += 1

                current_move_count = change_move_count

                if current_direction == 'LEFT':
                    current_direction = 'UP'
                elif current_direction == 'RIGHT':
                    current_direction = 'DOWN'
                elif current_direction == 'UP':
                    current_direction = 'RIGHT'
                elif current_direction == 'DOWN':
                    current_direction = 'LEFT'

    def heuristic(self, board):
        postive_factor = (find_doubles('G', board) +
                          150 * (find_triples('G', board) +
                          95 * find_quartets('G', board)))
        negative_factor = (find_doubles('X', board) +
                           150 * (find_triples('X', board) +
                           95 * find_quartets('X', board)))

        adversarial_pieces = find_all_pieces('X', board)/(BOARD_SIZE**2)
        return postive_factor - adversarial_pieces * negative_factor
