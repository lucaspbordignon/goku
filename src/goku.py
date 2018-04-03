from constants import BOARD_SIZE
import numpy as np
import regex as re


# TODO: Return the position for the next move, not only the heuristic value


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
            # TODO: Change this value to '- infinity'
            value = -100000
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
            # TODO: Change this value to '+ infinity'
            value = 1000000000
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
        postive_factor = (self.find_doubles('G', board) +
                          150 * self.find_triples('G', board) +
                          95 * self.find_quartets('G', board))
        negative_factor = (self.find_doubles('X', board) +
                           150 * self.find_triples('X', board) +
                           95 * self.find_quartets('X', board))

        return postive_factor - 0.5 * negative_factor

    def find_doubles(self, symbol, board):
        doubles = 0

        # Search for the rows
        for row in board:
            row_string = ''.join(row)
            doubles += len(re.findall(r'[' + symbol + r']{2}',
                           row_string,
                           overlapped=True))

        # Search for the columns
        for column in np.transpose(board):
            col_string = ''.join(column)
            doubles += len(re.findall(r'[' + symbol + r']{2}',
                           col_string,
                           overlapped=True))

        # Search for the first diagonal direction
        index = - (BOARD_SIZE + 1)
        while index < BOARD_SIZE:
            diagonal_string = ''.join(board.diagonal(index))
            doubles += len(re.findall(r'[' + symbol + r']{2}',
                           diagonal_string,
                           overlapped=True))
            index += 1

        # Search for the other direction
        index = - (BOARD_SIZE + 1)
        flipped_board = np.fliplr(board)
        while index < BOARD_SIZE:
            diagonal_string = ''.join(flipped_board.diagonal(index))
            doubles += len(re.findall(r'[' + symbol + r']{2}',
                           diagonal_string,
                           overlapped=True))
            index += 1
        return doubles

    def find_triples(self, symbol, board):
        triples = 0

        # Search for the rows
        for row in board:
            row_string = ''.join(row)
            triples += len(re.findall(r'[' + symbol + r']{3}',
                           row_string,
                           overlapped=True))

        # Search for the columns
        for column in np.transpose(board):
            col_string = ''.join(column)
            triples += len(re.findall(r'[' + symbol + r']{3}',
                           col_string,
                           overlapped=True))

        # Search for the first diagonal direction
        index = - (BOARD_SIZE + 1)
        while index < BOARD_SIZE:
            diagonal_string = ''.join(board.diagonal(index))
            triples += len(re.findall(r'[' + symbol + r']{3}',
                           diagonal_string,
                           overlapped=True))
            index += 1

        # Search for the other direction
        index = - (BOARD_SIZE + 1)
        flipped_board = np.fliplr(board)
        while index < BOARD_SIZE:
            diagonal_string = ''.join(flipped_board.diagonal(index))
            triples += len(re.findall(r'[' + symbol + r']{3}',
                           diagonal_string,
                           overlapped=True))
            index += 1
        return triples

    def find_quartets(self, symbol, board):
        quartets = 0

        # Search for the rows
        for row in board:
            row_string = ''.join(row)
            quartets += len(re.findall(r'[' + symbol + r']{4}',
                            row_string,
                            overlapped=True))

        # Search for the columns
        for column in np.transpose(board):
            col_string = ''.join(column)
            quartets += len(re.findall(r'[' + symbol + r']{4}',
                            col_string,
                            overlapped=True))

        # Search for the first diagonal direction
        index = - (BOARD_SIZE + 1)
        while index < BOARD_SIZE:
            diagonal_string = ''.join(board.diagonal(index))
            quartets += len(re.findall(r'[' + symbol + r']{4}',
                            diagonal_string,
                            overlapped=True))
            index += 1

        # Search for the other direction
        index = - (BOARD_SIZE + 1)
        flipped_board = np.fliplr(board)
        while index < BOARD_SIZE:
            diagonal_string = ''.join(flipped_board.diagonal(index))
            quartets += len(re.findall(r'[' + symbol + r']{4}',
                            diagonal_string,
                            overlapped=True))
            index += 1
        return quartets
