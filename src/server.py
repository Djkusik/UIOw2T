import asyncio

from api import api_server
from game import WaitingRoom


def main() -> None:
    waiting_room = WaitingRoom()

    loop = asyncio.get_event_loop()
    loop.create_task(api_server(waiting_room))
    loop.run_until_complete(waiting_room.start_games())
    loop.close()


if __name__ == "__main__":
    main()
