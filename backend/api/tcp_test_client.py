import socket

from api.communication.Requests import NewPlayerRequest
import json

HOST = '127.0.0.1'
PORT = 8081

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    request = NewPlayerRequest('TEST')
    json_string = json.dumps(request.__dict__)
    s.sendall(json_string.encode())
    data = s.recv(1024)

print('Received', repr(data))
