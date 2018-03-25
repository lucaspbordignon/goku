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
        self._running = True
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
        while self._running:
            move = self._render_game(mode)
            self._mark_board(self._actual_player, move)
            self._toggle_player()

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
        self._board[position] = self._players[self._actual_player]

    def _game_finished(self):
        return self._check_row() \
                or self._check_column() \
                or self._check_diagonal()

    def _check_row(self):
        """
            Checks if the board is finished. i.e. some player has made
            5 in a row
        """
        pass

    def _check_column(self):
        """
            Checks if the board is finished. i.e. some player has made
            5 in a column
        """
        pass

    def _check_diagonal(self):
        """
            Checks if the board is finished. i.e. some player has made
            5 in a diagonal
        """
        pass
