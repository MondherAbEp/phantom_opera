from .character import DefaultCharacter
from .game_status import GameStatus


# Initial status of the game
class InitialStatus(GameStatus):

    def __init__(self, game_state):

        super().__init__()
        self.passages = [
            (1, 4), (0, 2), (1, 3), (2, 7), (0, 5, 8),
            (4, 6), (5, 7), (3, 6, 9), (4, 9), (7, 8)
        ]

        self.pink_passages = [
            (1, 4), (0, 2, 5, 7), (1, 3, 6), (2, 7), (0, 5, 8, 9),
            (4, 6, 1, 8), (5, 7, 2, 9), (3, 6, 9, 1), (4, 9, 5), (7, 8, 4, 6)
        ]
        self.is_root = True
        game_state['root_node'] = InitialStatus
        self.predictions = []
        self.best = None
        self.process_prediction(0, game_state)

    def process_prediction(self, id, game_state):
        ch = game_state['options'][id]
        color = ch['color']
        routes = self.passages[ch['position']] if color != 'pink' else \
            self.pink_passages[ch['position']]
        tmp = DefaultCharacter(game_state, color, routes)
        tmp.options_index = id
        # if ch['position'] in game_state['blocked']:
        #     routes = [r for r in routes if r not in game_state['blocked']]
        if self.best is None or abs(tmp.get_best_gain()) < abs(
                self.best.get_best_gain()):
            self.best = tmp
        self.predictions.append(tmp)
        if id + 1 < len(game_state['options']): self.process_prediction(id + 1, game_state)
