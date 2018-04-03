import numpy as np

BOARD_SIZE = 15
EXIT = 'get out'
INITIAL_MENU = {
    0: 'Exit',
    1: 'Play Human vs Human',
}

INITIAL_BOARD = np.full((BOARD_SIZE, BOARD_SIZE), '.')
WIN_REGEX = r'([X]{5})|([O]{5})|([G]{5})'
