import copy
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

    def evaluate(self, active_pieces):
        black_team, white_team = self.eval.evaluate(active_pieces)
        return black_team, white_team

    def get_possible_moves(self, board, pieces):
        self.move_to_do = None
        self.move_to_do = self.minimax(board, pieces, self.depth, True) 
        print(self.move_to_do)
        input()
        return self.move_to_do

    def generate_all_moves(self, team, board, pieces):
        moves = []
        for piece in pieces:
            if piece.team == team:
                valid_moves = piece.valid_moves(board, pieces)  # returns list of (row, col)
                for move in valid_moves:
                    moves.append(((piece.row, piece.col), move))
        return moves

    def minimax(self, board, pieces, depth, is_maximizing):
        if depth == 0 or self.is_game_over(pieces):
            return self.eval.evaluate(pieces)

        team = self.team if is_maximizing else self.get_opponent_team()
        all_moves = self.generate_all_moves(team, board, pieces)
        return all_moves

        if is_maximizing:
            max_eval = float('-inf')
            for from_pos, to_pos in all_moves:
                new_board, new_pieces = self.simulate_move(from_pos, to_pos, board, pieces)
                eval_score = self.minimax(new_board, new_pieces, depth - 1, False)
                if eval_score > max_eval:
                    max_eval = eval_score
                    if depth == self.depth:
                        self.move_to_do = (from_pos, to_pos)  # <-- your tuple here
            return max_eval
        else:
            min_eval = float('inf')
            for from_pos, to_pos in all_moves:
                new_board, new_pieces = self.simulate_move(from_pos, to_pos, board, pieces)
                eval_score = self.minimax(new_board, new_pieces, depth - 1, True)
                if eval_score < min_eval:
                    min_eval = eval_score
            return min_eval

    def simulate_move(self, from_pos, to_pos, board, pieces):
        board_copy = copy.deepcopy(board)
        pieces_copy = copy.deepcopy(pieces)

        # Move the piece
        for piece in pieces_copy:
            if (piece.row, piece.col) == from_pos:
                piece.move(to_pos[0], to_pos[1])
                break

        # Remove captured piece, if any
        for piece in pieces_copy:
            if (piece.row, piece.col) == to_pos and (piece.row, piece.col) != from_pos:
                pieces_copy.remove(piece)
                break

        # Update the board
        board_copy[to_pos[0]][to_pos[1]] = board_copy[from_pos[0]][from_pos[1]]
        board_copy[from_pos[0]][from_pos[1]] = None

        return board_copy, pieces_copy

    def get_opponent_team(self):
        return 'b' if self.team == 'r' else 'r'

    def is_game_over(self, pieces):
        # Basic check: no opponent pieces left
        return not any(p.team == self.get_opponent_team() for _, p in pieces)
