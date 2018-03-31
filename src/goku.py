from constants import BOARD_SIZE
import numpy as np
import regex as re


class Goku:
    """
        Implements the AI agent for the gomoku game. It uses the minimax
    algorithm to find the best option for the next move, using alpha-beta
    pruning
    """

    def __init__(self, board):
        self._board = board

    def search(self, state, max_level=3):
        """
            1 - Makes a depth-first-search till raise the max_level of the tree
            2 - When got to the max_level, computes the heuristic(because
            the game is not finished yet, probably)
            3 - Recursively updates the parent nodes alha/beta with the right
            values
            4 - Make the pruning when needed
            5 - After compute 'all' the possibilities, return the next movement
        """
        pass

    def heuristic(self, state):
        postive_factor = (self.find_doubles('G') +
                          150 * self.find_triples('G') +
                          95 * self.find_quartets('G'))
        negative_factor = (self.find_doubles('X') +
                           150 * self.find_triples('X') +
                           95 * self.find_quartets('X'))

        return postive_factor - 0.5 * negative_factor

    def utility(self, state):
        pass

    def find_doubles(self, symbol):
        doubles = 0

        # Search for the rows
        for row in self._board:
            row_string = ''.join(row)
            doubles += len(re.findall(r'[' + symbol + r']{2}',
                           row_string,
                           overlapped=True))

        # Search for the columns
        for column in np.transpose(self._board):
            col_string = ''.join(column)
            doubles += len(re.findall(r'[' + symbol + r']{2}',
                           col_string,
                           overlapped=True))

        # Search for the first diagonal direction
        index = - (BOARD_SIZE + 1)
        while index < BOARD_SIZE:
            diagonal_string = ''.join(self._board.diagonal(index))
            doubles += len(re.findall(r'[' + symbol + r']{2}',
                           diagonal_string,
                           overlapped=True))
            index += 1

        # Search for the other direction
        index = - (BOARD_SIZE + 1)
        flipped_board = np.fliplr(self._board)
        while index < BOARD_SIZE:
            diagonal_string = ''.join(flipped_board.diagonal(index))
            doubles += len(re.findall(r'[' + symbol + r']{2}',
                           diagonal_string,
                           overlapped=True))
            index += 1
        return doubles

    def find_triples(self, symbol):
        pass

    def find_quartets(self, symbol):
        pass
