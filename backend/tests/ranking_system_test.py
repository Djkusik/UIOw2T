import unittest
import os
from db import Database, PlayerRankingRepository
from game.models.player import Player
from game.ranking.ranking_system import RankingSystem


class RankingSystemTest(unittest.TestCase):
    def setUp(self) -> None:
        self.db = Database('database.db')
        self.repository = PlayerRankingRepository(self.db)
        self.ranking_system = RankingSystem(self.repository)

    def tearDown(self) -> None:
        self.db.conn.close()
        os.remove('database.db')

    def test_4p(self):
        # given
        players = [Player('test1', 'x1'), Player('test2', 'x2'), Player('test3', 'x3'), Player('test4', 'x4')]
        result = [1050, 1025, 975, 950]

        # when
        self.ranking_system.calculate_ranking_points(players)

        # then
        for i, pack in enumerate(self.repository.read_all()):
            nick = pack[0]
            elo = pack[1]
            self.assertEqual(nick, players[i].nick)
            self.assertEqual(elo, result[i])

