import asyncio

from api import api_server
from game import Game


def main() -> None:
    game = Game()

    loop = asyncio.get_event_loop()
    loop.create_task(api_server(game))
    loop.run_until_complete(game.play())
    loop.close()


if __name__ == "__main__":
    main()
