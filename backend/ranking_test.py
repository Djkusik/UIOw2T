from typing import Tuple

from game.models.player import Player
import db
from game.ranking.ranking_system import RankingSystem

p1 = Player('test1', 'x1')
p2 = Player('test2', 'x2')
db = db.Database('data.db')
repo = db.PlayerRankingRepository(db)
ranking = RankingSystem(repo)

ranking.calculate_ranking_points(p1, Tuple[p1, p2])
