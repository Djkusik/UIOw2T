import aiohttp_cors

from .controllers import add_player


def setup_routes(app):
    app.router.add_post("/add_player", add_player)

    cors = aiohttp_cors.setup(
        app,
        defaults={
            "*": aiohttp_cors.ResourceOptions(
                allow_credentials=True, expose_headers="*", allow_headers="*"
            )
        },
    )

    for route in app.router.routes():
        cors.add(route)
