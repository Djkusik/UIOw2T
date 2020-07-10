import json
import sys

import socketio
from api.route_constants import *


def start_game(sid):
    for i in range(2):
        category = ""
        while category not in ("archer", "mage", "warrior"):
            category = input("Which unit do you want to place (archer/warrior/mage)?")
        coords = {"x": -1, "y": -1}
        while not (coords["x"] in range(0,8) and coords["y"] in range(0,4)):
            coords_input = input("Coordinates for the unit (eg. '3,2', x in 0-7, y in 0-3): ")
            try:
                coords_int = [int(x) for x in coords_input.split(",")]
            except:
                continue
            coords["x"], coords["y"] = coords_int[0], coords_int[1]

        sio.emit(UNIT, data={
            'class': category,
            'position': coords
        })

    sio.emit(UNITS_READY)
    print("Units ready.")
    sio.emit(QUESTIONS, data={"num": 2})


def answer_questions(data):
    score = 0
    print("Answer these 2 questions to determine your power-ups")
    correct = []
    for question in data:
        print(question["question"])
        for i, answer in enumerate(question["answers"]):
            print(f"{i})", answer["answer"])
            if answer["is_correct"]:
                correct.append(i)
        answers = []
        while not answers:
            try:
                answers = input("Your answers (write as e.g. '2,4,6'): ")
                answers = [int(x) for x in answers.split(",")]
            except:
                continue
        if any([a not in correct for a in answers]) or len(correct) - len(answers) > 1 or len(answers) == 0:
            score += 0
        elif len(correct) - len(answers) == 1:
            score += 1
        else:
            score += 2
        print("Correct answers were:", correct)

    print("YOUR SCORE:", score)
    sio.emit(SCORE, data={'score': score})


def on_game_result(data):
    print("GAME RESULT:", data["message"])
    with open("battle-logs.json", 'w') as f:
        f.write(json.dumps(data["logs"], indent=4))
    print("Battle logs saved to battle-logs.json")
    sys.exit(0)


if __name__ == '__main__':
    sio = socketio.Client()
    sio.connect('http://localhost:8080')
    nick = input("Your nick: ")
    sio.emit(LOGIN, data={'nick': nick})
    sio.emit(PLAYERS)
    sio.emit(PLAYERS_WAITING)

    sio.on(QUESTIONS_REPLY, answer_questions)
    sio.on(GAME_STARTED, start_game)
    sio.on(GAME_RESULT, on_game_result)

    sio.on(LOGIN_REPLY, lambda data: print(data))
    sio.on(BATTLE_STARTED, lambda data: print(data))
    sio.on(SCORE_REPLY, lambda data: print(data))
    sio.on(UNIT_REPLY, lambda data: print(data))
    sio.on(PLAYERS_REPLY, lambda data: print(data))
    sio.on(PLAYERS_WAITING_REPLY, lambda data: print(data))
    sio.on(ERROR, lambda data: print(data))
    sio.wait()
