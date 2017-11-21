"""This file is provided as a starting template for writing your own unit
tests to run and debug your minimax and alphabeta agents locally.  The test
cases used by the project assistant are not public.
"""

import unittest

import isolation
import game_agent

from importlib import reload


class IsolationTest(unittest.TestCase):
    """Unit tests for isolation agents"""

    def setUp(self):
        reload(game_agent)
        self.player1 = "Player1"
        self.player2 = "Player2"
        self.game = isolation.Board(self.player1, self.player2)


class MiniMaxPlayerTest(unittest.TestCase):

    def setUp(self):
        reload(game_agent)
        self.player1 = game_agent.MinimaxPlayer()
        self.player2 = game_agent.MinimaxPlayer()
        self.game = isolation.Board(self.player1, self.player2)

    def test_minimax_returns_move(self):
        def timeout(): return 3
        move = self.player1.get_move(self.game, timeout)
        self.assertIsNotNone(move)
        self.assertIsInstance(move, tuple)
        self.assertIsNot(move, (-1, -1))

    def test_minimax_returns_illegal_move_when_timeout_returns_zero(self):
        def timeout(): return 0
        move = self.player1.get_move(self.game, timeout)
        self.assertIsNotNone(move)
        self.assertIsInstance(move, tuple)
        self.assertEqual(move, (-1, -1))


if __name__ == '__main__':
    unittest.main()
