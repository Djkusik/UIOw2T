import socketio
import sys

if __name__ == '__main__':
    sio = socketio.Client()
    sio.connect('http://localhost:8080')
    sio.emit('login', data={'nick': sys.argv[1]})
    sio.emit('questions', data={'num': 5})
    sio.emit('score', data={'score': 3})
    sio.emit('unit', data={
        'class': 'archer',
        'position': {'x': 2, 'y': 1}
    })
    sio.emit('unit', data={
        'class': 'warrior',
        'position': {'x': 3, 'y': 3}
    })
    sio.emit('players')
    sio.emit('players_waiting')
    sio.on('login_reply', lambda data: print(data))
    sio.on('questions_reply', lambda data: print(data))
    sio.on('score_reply', lambda data: print(data))
    sio.on('players_reply', lambda data: print(data))
    sio.on('players_waiting_reply', lambda data: print(data))
    sio.on('game_started', lambda data: print(data))
    sio.on('error', lambda data: print(data))
    sio.wait()
