from enum import IntEnum
import numpy as np
import regex as re
import time

from constants import BOARD_SIZE, INITIAL_BOARD, INITIAL_MENU, WIN_REGEX
from goku import Goku
from utils import find_quintuplets


class Human:
    def __init__(self, name):
        self.name = name

    def next_move(self, board):
        while True:
            print('Type the ROW to put your piece:')
            row = input('>>> ')
            print('Type the COLUMN to put your piece:')
            col = input('>>> ')

            try:
                return int(row), int(col)
            except ValueError:
                print('You must specify numbers.')


SYMBOLS = {
        None: '.',
        0: 'X',
        1: 'O',
        }


class Gomoku:
    """
        This class contains all the components needed to run the base game.
        It should not have any AI related functionality.
    """
    def __init__(self):
        self.board = np.full((BOARD_SIZE, BOARD_SIZE), None)
        self._menu = INITIAL_MENU

    def run(self):
        self.render()

    def render(self, skip_menu=False):
        if True:
        # try:
            if not skip_menu:
                self._render_menu()
                self._game_mode = int(input('>>> '))
            if self._game_mode != 0:
                self._start_game([Human('Player 1'), Goku(0, 1)])
        # except ValueError:
        #     print('\nThe given option was not a number!')
        #     self.render(skip_menu=True)

    def _start_game(self, players):
        self.players = players
        self.current_player = 0

        while not self.game_finished((self.current_player - 1) % len(players)):
            self.render_board()
            current_player = players[self.current_player]

            start = time.time()
            move = current_player.next_move(self.board)
            print(move)

            if not self.mark_board(self.current_player, move):
                print('Position already in use or out of the board!')
                continue

            print('Execution time: %f' % (time.time() - start))
            self.toggle_player()

        self.render_board()
        print('We have a winner')

    def _render_menu(self):
        print('Welcome to the awesome Gomoku game!')
        for key, text in self._menu.items():
            print('Type {} to: {}'.format(key, text))

    def render_board(self):
        """
            Only renders de game board on the screen with coordinates
        """
        print('   ', end='')
        for i in range(len(self.board)):
            print(i, end='  ') if i < 10 else print(i, end=' ')
        print()
        for index, row in enumerate(self.board):
            print(index, end='  ') if index < 10 else print(index, end=' ')
            list(map(lambda x: print(SYMBOLS[x], end='  '), row))
            print()

    def toggle_player(self):
        self.current_player = (self.current_player + 1) % len(self.players)

    def mark_board(self, player, position):
        if not self.is_valid_position(position) or \
                self.board[position] is not None:
            return False
        self.board[position] = player
        return True

    def game_finished(self, next_player):
        return find_quintuplets(next_player, self.board) > 0

    def is_valid_position(self, position):
        x_coord, y_coord = position
        return 0 <= x_coord <= BOARD_SIZE and 0 <= y_coord <= BOARD_SIZE
