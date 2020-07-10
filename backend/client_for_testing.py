import sys

import socketio
from api.route_constants import *


def start_game(sid):
    sio.emit(QUESTIONS, data={'num': 5})
    sio.emit(SCORE, data={'score': 3})
    sio.emit(UNITS_FROM_SHOP)
    sio.emit(UNIT, data={
        'class': 'archer',
        'position': {'x': 2, 'y': 1}
    })
    sio.emit(UNIT, data={
        'class': 'warrior',
        'position': {'x': 3, 'y': 3}
    })
    sio.emit(UNITS_READY)


if __name__ == '__main__':
    sio = socketio.Client()
    sio.connect('http://localhost:8080')
    nick = 'Tomusz' if len(sys.argv) <= 1 else sys.argv[1]
    sio.emit(LOGIN, data={'nick': nick})
    sio.emit(PLAYERS)
    sio.emit(PLAYERS_WAITING)

    sio.on(GAME_STARTED, start_game)

    sio.on(LOGIN_REPLY, lambda data: print(data))
    sio.on(BATTLE_STARTED, lambda data: print(data))
    sio.on(QUESTIONS_REPLY, lambda data: print(data))
    sio.on(SCORE_REPLY, lambda data: print(data))
    sio.on(UNIT_REPLY, lambda data: print(data))
    sio.on(PLAYERS_REPLY, lambda data: print(data))
    sio.on(PLAYERS_WAITING_REPLY, lambda data: print(data))
    sio.on(ERROR, lambda data: print(data))
    sio.on(GAME_RESULT, lambda data: print(data))
    sio.on(UNITS_FROM_SHOP_REPLY, lambda data: print(data))
    sio.wait()
