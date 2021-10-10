import json
import random
import socket

import protocol
from lolemo_src.game_score_computation import (
    fantom_gain as fantom,
    inspector_gain as inspector
)
from lolemo_src.initial_status import InitialStatus

host = "localhost"
port = 12000


class Player:

    def __init__(self):

        self.end = False
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.game_state = None
        self.tree = None
        self.intents = {
            4: [fantom, inspector, inspector, fantom],
            3: [fantom, fantom, inspector],
            2: [fantom, inspector],
            1: [fantom]
        }

    def predict_round(self, options):
        self.game_state['options'] = options
        self.game_state['compute_gain'] = self.intents[len(options)]

        self.tree = InitialStatus(self.game_state)

        return self.tree.best.options_index

    def send_position(self, options) -> int:
        index = options.index(self.tree.get_move_target())
        return index

    def connect(self):
        self.socket.connect((host, port))

    def reset(self):
        self.socket.close()

    def answer(self, question):
        data = question["data"]
        self.game_state = question["game state"]

        response_index = random.randint(0, len(data) - 1)

        qt = question['question type']
        if qt.startswith('select character'):
            try:
                return self.predict_round(data)
            except:
                pass
        if qt.startswith('select position'):
            try:
                return self.send_position(data)
            except:
                pass
        return response_index

    def handle_json(self, data):
        data = json.loads(data)
        response = self.answer(data)
        bytes_data = json.dumps(response).encode("utf-8")
        protocol.send_json(self.socket, bytes_data)

    def run(self):

        self.connect()

        while self.end is not True:
            received_message = protocol.receive_json(self.socket)
            if received_message:
                self.handle_json(received_message)
            else:
                print("no message, finished learning")
                self.end = True


p = Player()

p.run()
