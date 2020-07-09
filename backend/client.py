import sys

import socketio
from .api.routes import *

if __name__ == '__main__':
    sio = socketio.Client()
    sio.connect('http://localhost:8080')
    nick = 'Tomusz' if len(sys.argv) <= 1 else sys.argv[1]
    sio.emit(LOGIN, data={'nick': nick})
    sio.emit(QUESTIONS, data={'num': 5})
    sio.emit(SCORE, data={'score': 3})
    sio.emit(UNIT, data={
        'class': 'archer',
        'position': {'x': 2, 'y': 1}
    })
    sio.emit(UNIT, data={
        'class': 'warrior',
        'position': {'x': 3, 'y': 3}
    })
    sio.emit(PLAYERS)
    sio.emit(PLAYERS_WAITING)
    sio.on(LOGIN_REPLY, lambda data: print(data))
    sio.on(QUESTIONS_REPLY, lambda data: print(data))
    sio.on(SCORE_REPLY, lambda data: print(data))
    sio.on(UNIT_REPLY, lambda data: print(data))
    sio.on(PLAYERS_REPLY, lambda data: print(data))
    sio.on(PLAYERS_WAITING_REPLY, lambda data: print(data))
    sio.on(GAME_STARTED, lambda data: print(data))
    sio.on(ERROR, lambda data: print(data))
    sio.wait()
