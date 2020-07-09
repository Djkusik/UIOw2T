from .config import get_cors
from .controllers import SocketController

CONNECT = "connect"
DISCONNECT = "disconnect"
LOGIN = "login"
PLAYERS = "players"
PLAYERS_WAITING = "players_waiting"
QUESTIONS = "questions"
SCORE = "score"
UNIT = "unit"
ERROR = "error"
SCORE_REPLY = "score_reply"
LOGIN_REPLY = "login_reply"
PLAYERS_REPLY = "players_reply"
PLAYERS_WAITING_REPLY = "players_waiting_reply"
QUESTIONS_REPLY = "questions_reply"
UNIT_REPLY = "unit_reply"
GAME_STARTED = "game_started"
GAME_RESULT = "game_result"


def setup_routes(app, sio, game_app):
    socket_controller = SocketController(sio, game_app)
    sio.on(CONNECT, socket_controller.on_socket_connected)
    sio.on(DISCONNECT, socket_controller.on_socket_disconnected)
    sio.on(LOGIN, socket_controller.on_socket_login)
    sio.on(PLAYERS, socket_controller.get_players)
    sio.on(PLAYERS_WAITING, socket_controller.get_players_in_waiting_room)
    sio.on(QUESTIONS, socket_controller.get_questions)
    sio.on(SCORE, socket_controller.save_quiz_score)
    sio.on(UNIT, socket_controller.add_unit)

    cors = get_cors(app)
    for route in app.router.routes():
        if route.resource.canonical == "/socket.io/":
            continue
        cors.add(route)
