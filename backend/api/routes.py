from .controllers import add_player, get_questions
from .config import get_cors


def setup_routes(app):
    app.router.add_post("/add_player", add_player)
    app.router.add_get("/questions", get_questions)
    cors = get_cors(app)
    for route in app.router.routes():
        cors.add(route)
