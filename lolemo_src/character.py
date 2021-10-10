from copy import deepcopy

from .game_status import GameStatus
from .move_character import MoveCharacter


# Default character class
class DefaultCharacter(GameStatus):

    def __init__(self, game_state: dict, character_color: str, moves: list):
        GameStatus.__init__(self)
        self.is_root = True

        self.game_state = deepcopy(game_state)

        self.id = -1
        self.character = None
        for i, c in enumerate(self.game_state['characters']):
            if c['color'] == character_color:
                self.id = i
                self.character = c

        self.game_state['options'].pop(
            next(id for id, ch in enumerate(self.game_state['options']) if
                 ch['color'] == character_color)
        )

        for m in moves:
            tmp = MoveCharacter(self.game_state, self.id, m)
            if self.best is None or tmp.gain > self.best.gain:
                self.best = tmp
                self.gain = tmp.gain
            self.options.append(tmp)
