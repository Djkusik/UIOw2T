import functools
from .config import get_cors
from .controllers import add_player, get_questions, add_player_to_waiting_room, get_players, \
    get_players_in_waiting_room, on_socket_connected, on_socket_login, on_socket_disconnected


def setup_routes(app, sio, game_app):
    app.router.add_post("/add_player", add_player)
    app.router.add_post("/add_player_to_waiting_room", add_player_to_waiting_room)
    app.router.add_get("/questions", get_questions)
    app.router.add_get("/players", get_players)
    app.router.add_get("/players_in_waiting_room", get_players_in_waiting_room)

    sio.on("connect", functools.partial(on_socket_connected, sio=sio, game_app=game_app))
    sio.on("login", functools.partial(on_socket_login, sio=sio, game_app=game_app))
    sio.on("disconnect", functools.partial(on_socket_disconnected, sio=sio, game_app=game_app))

    cors = get_cors(app)
    for route in app.router.routes():
        if route.resource.canonical == "/socket.io/":
            continue
        cors.add(route)
