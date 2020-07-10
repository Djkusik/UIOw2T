import asyncio
from socketio import AsyncServer

from api import api_server
from game import GameApp



def main() -> None:
    sio = AsyncServer(cors_allowed_origins='*')
    game_app = GameApp()
    loop = asyncio.get_event_loop()
    loop.create_task(api_server(game_app, sio))
    loop.run_until_complete(game_app.start_games())
    loop.close()


if __name__ == "__main__":
    main()
