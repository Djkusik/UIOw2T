import json
import logging
import random
from socketio import AsyncServer
from aiofile import AIOFile
from game import GameApp


class SocketController:
    def __init__(self, sio: AsyncServer, game_app: GameApp):
        self.sio: AsyncServer = sio
        self.game_app: GameApp = game_app

    async def on_socket_connected(self, sid, environ):
        logging.info(f"Got new connection from peer with SID: {sid}")
        pass

    async def on_socket_disconnected(self, sid):
        logging.info(f"Disconnected from peer with SID: {sid}")
        # TODO: handle disconnected
        pass

    async def on_socket_login(self, sid, data):
        if 'nick' not in data:
            await self.sio.emit("error", data={"message": "no login specified"}, room=sid)
            return
        player = self.game_app.add_player(data['nick'], sid)
        await self.sio.emit("login_reply", data={"message": "login ok"}, room=sid)
        logging.info(f"Added player '{player.nick}' with id '{player.id}' to the game")

        if self.game_app.is_waiting_room_full():
            await self.on_game_started()
            await self.game_app.start_games()

    async def get_players(self, sid):
        players = self.game_app.get_players()
        response = dict(players=[p.nick for p in players])
        await self.sio.emit('players_reply', data=response, room=sid)
        logging.info(f"Sent player info to peer with SID: {sid}")

    async def get_players_in_waiting_room(self, sid):
        players = self.game_app.get_players_in_waiting_room()
        response = dict(players_waiting=[p.nick for p in players])
        await self.sio.emit('players_waiting_reply', data=response, room=sid)
        logging.info(f"Sent waiting players info to peer with SID: {sid}")

    async def get_questions(self, sid, data):
        default_number = 3
        questions_path = "api/data/questions.json"

        # Get the requested number or use default
        num = data['num'] if 'num' in data else default_number
        logging.info(f"Getting {num} questions (default is {default_number})")
        try:
            num = int(num)
        except:
            num = default_number

        async with AIOFile(questions_path, 'r') as f:
            s = await f.read()
            questions = json.loads(s)
        response = random.sample(questions, num)
        await self.sio.emit('questions_reply', data=response, room=sid)
        logging.info(f"Sent {num} questions to peer with SID: {sid}")

    async def save_quiz_score(self, sid, data):
        if "score" not in data:
            await self.sio.emit("error", data={"message": "No quiz score provided"}, room=sid)
            return
        player = self.game_app.get_player_by_id(sid)
        player.quiz_score = data["score"]
        logging.info(f"Saved quiz score {data['score']} for player {player}")
        await self.sio.emit("score_reply", data={"message": "Score saved"}, room=sid)

    async def on_game_started(self):
        players = self.game_app.get_players()
        message = {'message': 'game started'}
        for player in players:
            await self.sio.emit('game_started', data=message, room=player.id)
            logging.info(f"Sent start game info to peer with SID: {player.id}")
