from .evaluation import Evalution

class Minimax:
    def __init__(self, team, pieces, board, depth=3):
        self.team = team
        self.pieces = pieces
        self.board = board
        self.depth = depth
        self.own_pieces = []
        self.__setup()
        self.move_to_do = None

        self.eval = Evalution()

    def __setup(self):
        self.own_pieces = [piece for team, piece in self.pieces if team == self.team]

    def get_valid_moves(self):
        pass

    def evaluate(self, active_pieces):
        black_team, white_team = self.eval.evaluate(active_pieces)
        return black_team, white_team