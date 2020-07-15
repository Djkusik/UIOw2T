import asyncio
from socketio import AsyncServer

from api import api_server
from db import Database, PlayerRankingRepository
from game import GameApp
from game.ranking.ranking_system import RankingSystem


def main() -> None:
    sio = AsyncServer(cors_allowed_origins='*')
    database = Database('data.db')
    player_ranking_repository = PlayerRankingRepository(database)
    ranking_system = RankingSystem(player_ranking_repository)
    game_app = GameApp()
    game_app.on_game_result = ranking_system.calculate_ranking_points
    loop = asyncio.get_event_loop()
    loop.create_task(api_server(game_app, sio,player_ranking_repository))
    loop.run_until_complete(game_app.start_games())
    loop.close()


if __name__ == "__main__":
    main()
