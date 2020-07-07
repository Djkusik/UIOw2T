import socketio
import time

if __name__ == '__main__':
    sio = socketio.Client()
    sio.connect('http://localhost:8080')
    sio.emit('login', data={'nick': 'artur2'})
    sio.emit('questions', data={'num': 5})
    sio.emit('players')
    sio.emit('players_waiting')
    sio.on('login_reply', lambda data: print(data))
    sio.on('questions_reply', lambda data: print(data))
    sio.on('players_reply', lambda data: print(data))
    sio.on('players_waiting_reply', lambda data: print(data))
    sio.on('game_started', lambda data: print(data))
    sio.on('error', lambda data: print(data))
    sio.wait()