import unittest
from pprint import pprint

import goku
from gomoku import Gomoku


class GokuTest(unittest.TestCase):
    def setUp(self):
        self.game = Gomoku()

    def test_find_doubles_col(self):
        game = self.game

        game._mark_board(player=0, position=(0, 0))
        game._mark_board(player=0, position=(1, 0))

        doubles = goku.find_doubles('X', game._board)
        self.assertEqual(doubles, 1)

        game._mark_board(player=0, position=(2, 0))

        doubles = goku.find_doubles('X', game._board)
        self.assertEqual(doubles, 2)

    def test_find_doubles_diag(self):
        game = self.game

        game._mark_board(player=0, position=(0, 0))
        game._mark_board(player=0, position=(1, 1))

        doubles = goku.find_doubles('X', game._board)
        self.assertEqual(doubles, 1)

        game._mark_board(player=0, position=(2, 2))

        doubles = goku.find_doubles('X', game._board)
        self.assertEqual(doubles, 2)

    def test_find_doubles_row(self):
        game = self.game

        game._mark_board(player=0, position=(0, 0))
        game._mark_board(player=0, position=(0, 1))

        doubles = goku.find_doubles('X', game._board)
        self.assertEqual(doubles, 1)

        game._mark_board(player=0, position=(0, 2))

        doubles = goku.find_doubles('X', game._board)
        self.assertEqual(doubles, 2)

    def test_find_triples_col(self):
        game = self.game

        game._mark_board(player=0, position=(0, 0))
        game._mark_board(player=0, position=(1, 0))
        game._mark_board(player=0, position=(2, 0))

        triples = goku.find_triples('X', game._board)
        self.assertEqual(triples, 1)

        game._mark_board(player=0, position=(3, 0))

        triples = goku.find_triples('X', game._board)
        self.assertEqual(triples, 2)

    def test_find_triples_row(self):
        game = self.game

        game._mark_board(player=0, position=(0, 0))
        game._mark_board(player=0, position=(0, 1))
        game._mark_board(player=0, position=(0, 2))

        triples = goku.find_triples('X', game._board)
        self.assertEqual(triples, 1)

        game._mark_board(player=0, position=(0, 3))

        triples = goku.find_triples('X', game._board)
        self.assertEqual(triples, 2)

    def test_find_quartets_col(self):
        game = self.game

        game._mark_board(player=0, position=(0, 0))
        game._mark_board(player=0, position=(1, 0))
        game._mark_board(player=0, position=(2, 0))
        game._mark_board(player=0, position=(3, 0))

        quartets = goku.find_quartets('X', game._board)
        self.assertEqual(quartets, 1)

        game._mark_board(player=0, position=(4, 0))

        quartets = goku.find_quartets('X', game._board)
        self.assertEqual(quartets, 2)

    def test_find_quartets_row(self):
        game = self.game

        game._mark_board(player=0, position=(0, 0))
        game._mark_board(player=0, position=(0, 1))
        game._mark_board(player=0, position=(0, 2))
        game._mark_board(player=0, position=(0, 3))

        quartets = goku.find_quartets('X', game._board)
        self.assertEqual(quartets, 1)

        game._mark_board(player=0, position=(0, 4))

        quartets = goku.find_quartets('X', game._board)
        self.assertEqual(quartets, 2)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
