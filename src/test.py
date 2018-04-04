import unittest

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

    def test_find_doubles_edge_diag(self):
        game = self.game

        game._mark_board(player=0, position=(0, 1))
        game._mark_board(player=0, position=(1, 0))

        doubles = goku.find_doubles('X', game._board)
        self.assertEqual(doubles, 1)

        game._mark_board(player=0, position=(13, 14))
        game._mark_board(player=0, position=(14, 13))

        doubles = goku.find_doubles('X', game._board)
        self.assertEqual(doubles, 2)

        game._mark_board(player=0, position=(0, 13))
        game._mark_board(player=0, position=(1, 14))

        doubles = goku.find_doubles('X', game._board)
        self.assertEqual(doubles, 3)

        game._mark_board(player=0, position=(13, 0))
        game._mark_board(player=0, position=(14, 1))

        doubles = goku.find_doubles('X', game._board)
        self.assertEqual(doubles, 4)

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

    def test_find_triples_diag(self):
        game = self.game

        game._mark_board(player=0, position=(0, 0))
        game._mark_board(player=0, position=(1, 1))
        game._mark_board(player=0, position=(2, 2))

        triples = goku.find_triples('X', game._board)
        self.assertEqual(triples, 1)

        game._mark_board(player=0, position=(3, 3))

        triples = goku.find_triples('X', game._board)
        self.assertEqual(triples, 2)

    def test_find_triples_edge_diag(self):
        game = self.game

        game._mark_board(player=0, position=(0, 2))
        game._mark_board(player=0, position=(1, 1))
        game._mark_board(player=0, position=(2, 0))

        triples = goku.find_triples('X', game._board)
        self.assertEqual(triples, 1)

        game._mark_board(player=0, position=(12, 14))
        game._mark_board(player=0, position=(13, 13))
        game._mark_board(player=0, position=(14, 12))

        triples = goku.find_triples('X', game._board)
        self.assertEqual(triples, 2)

        game._mark_board(player=0, position=(0, 12))
        game._mark_board(player=0, position=(1, 13))
        game._mark_board(player=0, position=(2, 14))

        triples = goku.find_triples('X', game._board)
        self.assertEqual(triples, 3)

        game._mark_board(player=0, position=(12, 0))
        game._mark_board(player=0, position=(13, 1))
        game._mark_board(player=0, position=(14, 2))

        triples = goku.find_triples('X', game._board)
        self.assertEqual(triples, 4)

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

    def test_find_quartets_diag(self):
        game = self.game

        game._mark_board(player=0, position=(0, 0))
        game._mark_board(player=0, position=(1, 1))
        game._mark_board(player=0, position=(2, 2))
        game._mark_board(player=0, position=(3, 3))

        quartets = goku.find_quartets('X', game._board)
        self.assertEqual(quartets, 1)

        game._mark_board(player=0, position=(4, 4))

        quartets = goku.find_quartets('X', game._board)
        self.assertEqual(quartets, 2)

    def test_find_quartets_edge_diag(self):
        game = self.game

        game._mark_board(player=0, position=(0, 3))
        game._mark_board(player=0, position=(1, 2))
        game._mark_board(player=0, position=(2, 1))
        game._mark_board(player=0, position=(3, 0))

        quartets = goku.find_quartets('X', game._board)
        self.assertEqual(quartets, 1)

        game._mark_board(player=0, position=(11, 14))
        game._mark_board(player=0, position=(12, 13))
        game._mark_board(player=0, position=(13, 12))
        game._mark_board(player=0, position=(14, 11))

        quartets = goku.find_quartets('X', game._board)
        self.assertEqual(quartets, 2)

        game._mark_board(player=0, position=(0, 11))
        game._mark_board(player=0, position=(1, 12))
        game._mark_board(player=0, position=(2, 13))
        game._mark_board(player=0, position=(3, 14))

        quartets = goku.find_quartets('X', game._board)
        self.assertEqual(quartets, 3)

        game._mark_board(player=0, position=(11, 0))
        game._mark_board(player=0, position=(12, 1))
        game._mark_board(player=0, position=(13, 2))
        game._mark_board(player=0, position=(14, 3))

        quartets = goku.find_quartets('X', game._board)
        self.assertEqual(quartets, 4)

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
