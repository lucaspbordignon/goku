import re
from constants import *
from pdb import *


class Gomoku:
    """
        This class contains all the components needed to run the base game.
        It should not have any AI related functionality.
    """
    def __init__(self):
        self._board = INITIAL_BOARD
        self._menu = INITIAL_MENU
        self._winner = None
        self._players = {
            0: 'X',
            1: 'O',
            2: 'G'  # Goku, the AI agent
        }
        self._actual_player = 0

    def run(self):
        self.render()

    def render(self):
        try:
            self._render_menu()
            self.game_mode = int(input('>>> '))
            if self.game_mode != 0 : self._start_game(self.game_mode)
        except ValueError:
            print('The given option was not a number')
            self.game_mode = int(input('>>> '))
            if self.game_mode != 0 : self._start_game(self.game_mode)

    def _start_game(self, mode=1):
        while not self._winner:
            move = self._render_game(mode)
            if not self._mark_board(self._actual_player, move):
                print('Position already in use!')
                continue
            self._toggle_player()
            self._winner = self._game_finished()
        print('We have a winner')

    def _render_menu(self):
        print('Welcome to the awesome Gomoku game!')
        for key, text in self._menu.items():
            print('Type {} to: {}'.format(key, text))

    def _render_game(self, mode):
        self._render_board()
        print('Type the ROW to put your piece:')
        row = input('>>> ')
        print('Type the COLUMN to put your piece:')
        col = input('>>> ')
        return(int(row), int(col))

    def _render_board(self):
        """
            Only renders de game board on the screen with coordinates
        """
        for index, row in enumerate(self._board):
            print(index, end='  ') if index < 10 else print(index, end=' ')
            list(map(lambda x: print(x, end='  '), row))
            print()
        print('   ', end='')
        for i in range(len(self._board)):
            print(i, end='  ') if i < 10 else print(i, end=' ')
        print()

    def _toggle_player(self):
        self._actual_player = 0 if self._actual_player else 1

    def _mark_board(self, player, position):
        if self._board[position] != '.': return False
        self._board[position] = self._players[self._actual_player]
        return True

    def _game_finished(self):
        return self._check_row() \
                or self._check_column() \
                or self._check_diagonal()

    def _check_row(self):
        """
            Checks if the board is finished. i.e. some player has made
            5 in a row.
            Returns the symbol of the winner player, if there is one
        """
        match = None
        for row in self._board:
            row_string = ''.join(row)
            match = re.search(WIN_REGEX, row_string)
            if match: return match.group()[0]
        return None

    def _check_column(self):
        """
            Checks if the board is finished. i.e. some player has made
            5 in a column
            Returns the symbol of the winner player, if there is one
        """
        for column in np.transpose(self._board):
            col_string = ''.join(column)
            match = re.search(WIN_REGEX, col_string)
            if match: return match.group()[0]
        return None

    def _check_diagonal(self):
        """
            Checks if the board is finished. i.e. some player has made
            5 in a diagonal
        """
        return None
