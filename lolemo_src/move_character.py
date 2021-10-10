from copy import deepcopy

from .game_status import GameStatus


# Calculates the state of the game for a given character's new position
class MoveCharacter(GameStatus):

    def __init__(self, game_state: dict, charid: int, pos: int):
        GameStatus.__init__(self)

        self.game_state = deepcopy(game_state)

        self.pos = pos

        self.character = self.game_state['characters'][charid]
        self.character['position'] = self.pos
        self.gain = self.game_state['compute_gain'].pop(0)(self.game_state)

        if len(self.game_state['options']) > 0:
            self.next = self.game_state['root_node'](self.game_state)

    def get_best_gain(self):
        return self.next.get_best_gain() if self.next is not None else self.gain

    def get_move_target(self):
        return self.pos
