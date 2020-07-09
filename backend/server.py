import asyncio

from api import api_server
from game import GameApp


def main() -> None:
    game_app = GameApp()
    loop = asyncio.get_event_loop()
    loop.create_task(api_server(game_app))
    loop.run_until_complete(game_app.start_games())
    loop.close()


if __name__ == "__main__":
    main()
