# Abstract class for nodes used to build our tree
class GameStatus:

    def __init__(self):
        self.options = []
        self.best = None
        self.gain = 0
        self.is_root = False
        self.next = None

    def get_best_gain(self):
        if self.best is None:
            return self.gain
        return self.best.get_best_gain()

    def get_move_target(self):
        return self.best.get_move_target() if self.best is not None else None

    def get_next_root_node(self):
        return self.next or self.get_next_root_node()
