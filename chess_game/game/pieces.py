class Piece:
    def __init__(self, team, type, row, col):
        self.piece_symbols = {
            "Pawn": "P",
            "Rook": "R",
            "Knight": "N",
            "Bishop": "B",
            "Queen": "Q",
            "King": "K",
        }

        if type not in self.piece_symbols:
            raise ValueError(f"Invalid Piece Type: {type}")

        self.team = team
        self.piece = type
        self.piece_symbol = f'{self.piece_symbols[type]}'

        self.pos = (row, col)

    def __str__(self):
        return f"{self.team} {self.piece} ({self.piece_symbol}). Pos: {self.pos}"
    
class Pawn(Piece):
    def __init__(self, team, row, col):
        self.type = 'Pawn'
        super().__init__(team, self.type, row, col)

    def valid_moves(self, board):
        moves = []
        row, col = self.pos
        direction = -1 if self.team == 'White' else 1

        next_row = row + direction

        # Check if next square forward is inside the board and empty
        if 0 <= next_row < 8 and not board[next_row][col]:
            moves.append((next_row, col))

            # Check if pawn is on starting row and can move 2 squares forward
            starting_row = 6 if self.team == 'White' else 1
            two_steps_row = row + 2 * direction
            if row == starting_row and not board[two_steps_row][col]:
                moves.append((two_steps_row, col))

        # (Later: add diagonal captures, en passant, promotion, etc.)

        return moves
    
class Knight(Piece):
    def __init__(self, team, row, col):
        super().__init__(team, 'Knight', row, col)

    def valid_moves(self, board):
        moves = []
        row, col = self.pos
        knight_moves = [
            (-2, -1), (-2, 1),
            (-1, -2), (-1, 2),
            (1, -2),  (1, 2),
            (2, -1),  (2, 1)
        ]

        for dr, dc in knight_moves:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                dest_piece = board[new_row][new_col]
                # If empty or opponent's piece, valid move
                if dest_piece is None or dest_piece.team != self.team:
                    moves.append((new_row, new_col))

        return moves
    
class Bishop(Piece):
    def __init__(self, team, row, col):
        self.type = 'Bishop'
        super().__init__(team, self.type, row, col)
    
    def valid_moves(self, board):
        moves = []
        row, col = self.pos
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc

            while 0 <= new_row < 8 and 0 <= new_col < 8:
                square = board[new_row][new_col]

                if square is None:
                    moves.append((new_row, new_col))
                elif square.team != self.team:
                    moves.append((new_row, new_col))
                    break
                else:  # square.team == self.team
                    break

                new_row += dr
                new_col += dc

        return moves

class Rook(Piece):
    def __init__(self, team, row, col):
        self.type = 'Rook'
        super().__init__(team, self.type, row, col)
    
    def valid_moves(self, board):
        moves = []
        row, col = self.pos
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # Down, Up, Right, Left

        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc

            while 0 <= new_row < 8 and 0 <= new_col < 8:
                square = board[new_row][new_col]

                if square is None:
                    moves.append((new_row, new_col))
                elif square.team != self.team:
                    moves.append((new_row, new_col))
                    break
                else:  # square.team == self.team
                    break

                new_row += dr
                new_col += dc

        return moves

class Queen(Piece):
    def __init__(self, team, row, col):
        self.type = 'Queen'
        super().__init__(team, self.type, row, col)
    
    def valid_moves(self, board):
        moves = []
        row, col = self.pos
        directions = [
            (1, 0), (-1, 0), (0, 1), (0, -1),  # Up, down, right, left
            (-1, -1), (-1, 1), (1, -1), (1, 1)  # Diagonals
        ]

        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc

            while 0 <= new_row < 8 and 0 <= new_col < 8:
                square = board[new_row][new_col]

                if square is None:
                    moves.append((new_row, new_col))
                elif square.team != self.team:
                    moves.append((new_row, new_col))
                    break
                else:  # square.team == self.team
                    break

                new_row += dr
                new_col += dc
        
        return moves

class King(Piece):
    def __init__(self, team, row, col):
        self.type = 'King'
        super().__init__(team, self.type, row, col)
    
    def valid_moves(self, board):
        pass
