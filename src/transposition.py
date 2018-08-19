import numpy as np
from constants import BOARD_SIZE


class TranspositionTable:
    def __init__(self):
        self._init_zobrist_hash()
        self._table = {}

    def contains(self, key):
        key in self._table

    def insert(self, key, value):
        self._table[key] = value

    def value(self, key):
        self._table[key]

    def hash_key(self, board):
        """
            Finds the hash key for a board state
        """
        hash_key = 0
        for position in np.argwhere(board != '.'):
            position = tuple(position)
            item_index = 0 if board[position] == 'G' else 1
            item_hash_value = int(self._zobrist_hash[position][item_index])
            hash_key = np.bitwise_xor(hash_key, item_hash_value)
        return hash_key

    def _init_zobrist_hash(self):
        """
            Creates a Zobrist Table, to extract the hash value of each
        board state of the game. i.e. creates BOARD_SIZE x BOARD_SIZE
        matrix with 2 random numbers each, as we have 2 symbols.
        """
        self._zobrist_hash = 1e6 * np.random.rand(BOARD_SIZE, BOARD_SIZE, 2)
