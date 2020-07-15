import math
from collections import Set

from db import PlayerRankingRepository
from game.models import Player


class RankingSystem:
    def __init__(self, player_repository: PlayerRankingRepository):
        self._player_repository = player_repository

    # pass player list, first one is winner, second one is second place etc
    # assigns points +K to first player, -K to last player, -K/2 to second player etc...
    def calculate_ranking_points(self, all_players):
        # map player to tuple [Player, current elo, probability of winning]
        K = 50
        DEFAULT_POINTS=1000

        player_points = ((p, self._player_repository.read(p.nick, DEFAULT_POINTS), 1 / len(all_players))
                         for p in all_players)
        points_added = list()
        for x in range(0,len(all_players)):
            points_added.append(0)
        i = 0
        for x in range(0, len(all_players) // 2):
            points_added[i] = K
            points_added[len(all_players) - 1 - i] = -K
            K = K / 2
            i = i + 1
        i = 0
        for (p, elo, probability) in player_points:
            self._player_repository.create_or_update(p.nick, elo + points_added[i])
            i = i + 1
        return list(player_points)

    def _probability_of_winning_elo(self, rating1, rating2):
        return 1.0 * 1.0 / (1 + 1.0 * math.pow(10, 1.0 * (rating1 - rating2) / 400))
