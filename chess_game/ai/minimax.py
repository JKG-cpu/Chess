class Minimax:
    def __init__(self, team, pieces, board, depth=3):
        self.team = team
        self.pieces = pieces
        self.board = board
        self.depth = depth
        self.own_pieces = []
        self.__setup()
        self.move_to_do = None

    def __setup(self):
        self.own_pieces = [piece for team, piece in self.pieces if team == self.team]

    def evaluate_board(self):
        piece_values = {'pawn':1, 'knight':3, 'bishop':3, 'rook':5, 'queen':9, 'king':1000}
        score = 0
        for pos, piece in self.board.get_all_pieces():
            if piece is None:
                continue
            value = piece_values.get(piece.type, 0)
            if piece.team == self.team:
                score += value
            else:
                score -= value
        return score

    def get_all_moves(self, team):
        moves = []
        for team_check, piece in self.pieces:
            if team_check == team:
                valid_moves = piece.valid_moves(self.board)
                for move in valid_moves:
                    moves.append((piece.pos, move))
        return moves

    def make_move(self, move):
        # move = (from_pos, to_pos)
        from_pos, to_pos = move
        piece = self.board.get_piece(from_pos)
        captured_piece = self.board.get_piece(to_pos)

        # Apply the move on the board & pieces
        self.board.move_piece(from_pos, to_pos)
        if captured_piece:
            self.pieces.remove((captured_piece.team, captured_piece))

        return captured_piece  # To undo later

    def undo_move(self, move, captured_piece):
        from_pos, to_pos = move
        piece = self.board.get_piece(to_pos)
        self.board.move_piece(to_pos, from_pos)
        if captured_piece:
            self.pieces.append((captured_piece.team, captured_piece))
            self.board.place_piece(captured_piece, to_pos)

    def minimax(self, depth, alpha, beta, maximizing_player):
        if depth == 0:
            return self.evaluate_board(), None

        team = self.team if maximizing_player else ('black' if self.team == 'white' else 'white')
        moves = self.get_all_moves(team)

        if not moves:
            # No moves = checkmate or stalemate, evaluate accordingly
            return self.evaluate_board(), None

        best_move = None

        if maximizing_player:
            max_eval = -float('inf')
            for move in moves:
                captured = self.make_move(move)
                eval_score, _ = self.minimax(depth-1, alpha, beta, False)
                self.undo_move(move, captured)
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = float('inf')
            for move in moves:
                captured = self.make_move(move)
                eval_score, _ = self.minimax(depth-1, alpha, beta, True)
                self.undo_move(move, captured)
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            return min_eval, best_move

    def get_best_move(self):
        _, best_move = self.minimax(self.depth, -float('inf'), float('inf'), True)
        self.move_to_do = best_move
        return best_move if best_move else 'Stalemate'
