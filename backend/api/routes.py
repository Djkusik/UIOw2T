from .config import get_cors
from .controllers import SocketController


def setup_routes(app, sio, game_app):
    socket_controller = SocketController(sio, game_app)
    sio.on("connect", socket_controller.on_socket_connected)
    sio.on("disconnect", socket_controller.on_socket_disconnected)
    sio.on("login", socket_controller.on_socket_login)
    sio.on("players", socket_controller.get_players)
    sio.on("players_waiting", socket_controller.get_players_in_waiting_room)
    sio.on("questions", socket_controller.get_questions)
    sio.on("score", socket_controller.save_quiz_score)
    sio.on("unit", socket_controller.add_unit)

    cors = get_cors(app)
    for route in app.router.routes():
        if route.resource.canonical == "/socket.io/":
            continue
        cors.add(route)
