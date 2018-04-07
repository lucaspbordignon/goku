import numpy as np

BOARD_SIZE = 15
EXIT = 'get out'
INITIAL_MENU = {
    0: 'Exit',
    1: 'Play Human vs Human',
    2: 'Play Human vs AI (Goku)'
}
DIRECTION_ENUM = {
    'UP': (0, -1),
    'DOWN': (0, 1),
    'LEFT': (-1, 0),
    'RIGHT': (1, 0)
}

DIRECTION_CHANGE_ENUM = {
    'UP': 'RIGHT',
    'DOWN': 'LEFT',
    'LEFT': 'UP',
    'RIGHT': 'DOWN'
}

INITIAL_BOARD = np.full((BOARD_SIZE, BOARD_SIZE), '.')
WIN_REGEX = r'([X]{5})|([O]{5})|([G]{5})'
