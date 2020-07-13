from typing import Tuple

from db import Database, PlayerRankingRepository
from game.models.player import Player
from game.ranking.ranking_system import RankingSystem

p1 = Player('test1', 'x1')
p2 = Player('test2', 'x2')
p3 = Player('test3', 'x3')
p4 = Player('test4', 'x4')
db = Database('data.db')
repo = PlayerRankingRepository(db)
ranking = RankingSystem(repo)

ranking.calculate_ranking_points({p1, p2,p3,p4})
for nick, elo in repo.read_all():
    print(f"{nick} : {elo}")

