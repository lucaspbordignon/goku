import math
import numpy as np
from constants import BOARD_SIZE
from constants import DIRECTION_ENUM
from utils import spiral_new_direction
from utils import sum_tuples
from utils import find_doublets
from utils import find_triplets
from utils import find_quartets
from transposition import TranspositionTable


class Goku:
    """
        Implements the AI agent for the gomoku game. It uses the minimax
    algorithm to find the best option for the next move, using alpha-beta
    pruning
    """

    def __init__(self):
        self._transposition_table = TranspositionTable()

    def next_move(self, board, max_level=4):
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
                max_level=4):
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
        """
            Makes a spiral movement through the board, starting from the center
        """
        repeating_positions = False
        central_index = BOARD_SIZE // 2
        current_position = (central_index, central_index)
        current_direction = 'DOWN'
        change_move_count = 1
        current_move_count = 1
        local_count = 2

        while not repeating_positions:
            current_move_count -= 1

            if board[current_position] == '.':
                yield current_position

            current_position = sum_tuples(current_position,
                                          DIRECTION_ENUM[current_direction])

            if BOARD_SIZE in current_position:
                repeating_positions = True

            if current_move_count == 0:
                local_count -= 1
                if not local_count:
                    local_count = 2
                    change_move_count += 1

                current_move_count = change_move_count
                current_direction = spiral_new_direction(current_direction)

    def heuristic(self, board):
        """
            The heuristic for the Goku agent. An estimative of how close
        we are to win the game, cause is the only thing that matters!
        """
        postive_factor = (find_doublets('G', board) +
                          150 * (find_triplets('G', board) +
                          95 * find_quartets('G', board)))
        negative_factor = (find_doublets('X', board) +
                           150 * (find_triplets('X', board) +
                           95 * find_quartets('X', board)))

        return postive_factor - 0.5 * negative_factor
