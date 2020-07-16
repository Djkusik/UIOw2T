from .config import get_cors
from .controllers import SocketController
from .route_constants import *


def setup_routes(app, sio, game_app,player_ranking_repository):
    socket_controller = SocketController(sio, game_app,player_ranking_repository)
    sio.on(CONNECT, socket_controller.on_socket_connected)
    sio.on(DISCONNECT, socket_controller.on_socket_disconnected)
    sio.on(LOGIN, socket_controller.on_socket_login)
    sio.on(PLAYERS, socket_controller.get_players)
    sio.on(PLAYERS_WAITING, socket_controller.get_players_in_waiting_room)
    sio.on(QUESTION, socket_controller.get_question)
    sio.on(SCORE, socket_controller.save_question_score)
    sio.on(ADD_UNITS, socket_controller.add_units)
    sio.on(UNITS_FROM_SHOP, socket_controller.get_shop_units)
    sio.on(GET_UNITS, socket_controller.get_units)
    sio.on(GET_GOLD, socket_controller.get_gold)
    sio.on(UNITS_READY, socket_controller.units_ready)
    sio.on(RANKING, socket_controller.ranking)

    cors = get_cors(app)
    for route in app.router.routes():
        if route.resource.canonical == "/socket.io/":
            continue
        cors.add(route)
