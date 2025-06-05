import os, time, random
from rich.console import Console
console = Console()

from ai import Minimax
from .pieces import *
from .move import Moves

def cc():
    os.system('cls' if os.name == 'nt' else 'clear')

class Board:
    def __init__(self):
        self.starting_positions = {
            "White-team":{
                'White': {
                    'Pawn':    [(6, i) for i in range(8)],
                    'Rook':    [(7, 0), (7, 7)],
                    'Knight':  [(7, 1), (7, 6)],
                    'Bishop':  [(7, 2), (7, 5)],
                    'Queen':   [(7, 3)],
                    'King':    [(7, 4)],
                },
                'Black': {
                    'Pawn':    [(1, i) for i in range(8)],
                    'Rook':    [(0, 0), (0, 7)],
                    'Knight':  [(0, 1), (0, 6)],
                    'Bishop':  [(0, 2), (0, 5)],
                    'Queen':   [(0, 3)],
                    'King':    [(0, 4)],
                }
            },
            'Black-team': {
                'Black': {
                    'Pawn':    [(6, i) for i in range(8)],
                    'Rook':    [(7, 0), (7, 7)],
                    'Knight':  [(7, 1), (7, 6)],
                    'Bishop':  [(7, 2), (7, 5)],
                    'Queen':   [(7, 3)],
                    'King':    [(7, 4)],
                },
                'White': {
                    'Pawn':    [(1, i) for i in range(8)],
                    'Rook':    [(0, 0), (0, 7)],
                    'Knight':  [(0, 1), (0, 6)],
                    'Bishop':  [(0, 2), (0, 5)],
                    'Queen':   [(0, 3)],
                    'King':    [(0, 4)],
                }
            },
            'Test-team': {
                'White': {
                    'King':  [(7, 4)],
                    'Queen': [(6, 4)],
                    'Rook':  [(5, 7)],
                    'Pawn': [(4, 4)]
                },
                'Black': {
                    'King':  [(0, 4)],
                    'Pawn': [(3, 3)]
                }
            }
        }

        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.empty = None
        self.active_pieces = []

        teams = ['White', 'Black']
        choice = 'White'
        self.team_setup = f'{choice}-team'
        self.team_setup = 'Test-team'
        self.team = f'{choice}'
        if self.team == 'White':
            self.op_team = 'Black'
        else:
            self.op_team = 'White'
        self.forward_direction = {
            "White": -1 if self.team == "White" else 1,
            "Black": 1 if self.team == "White" else -1
        }
        self.generate_board()
        
        self.moves = Moves(self.team)
        self.running = True
        self.playing = True
        self.turn = 'Player' if self.team == 'White' else "AI"

        self.ai = Minimax(self.op_team, self.active_pieces, self.board)

    # -------------------------------------------------- Generate Board / Pieces ---------------------------------------------
    def generate_board(self):
        cteam = self.starting_positions[self.team_setup]
        for team in cteam:
            for piece in cteam[team]:
                for row, col in cteam[team][piece]:
                    self.create_peice(piece, team, row, col)

    def create_peice(self, type, team, row, col):
        types = {
            'Pawn': Pawn,
            'Knight': Knight,
            'Bishop': Bishop,
            'Rook': Rook,
            'Queen': Queen,
            'King': King
        }

        if type not in types:
            raise TypeError(f"Type {type} is not a valid piece.")

        direction = self.forward_direction[team]

        # Only pass direction if it's a Pawn
        if type == 'Pawn':
            piece = types[type](team, row, col, direction)
        else:
            piece = types[type](team, row, col)

        self.active_pieces.append((team, piece))
        self.board[row][col] = piece

    # -------------------------------------------------- Play Chess Part -----------------------------------------------------
    def move_piece(self, from_r, from_c, to_r, to_c):
        piece = self.board[from_r][from_c]
        spot = self.board[to_r][to_c]
        if isinstance(spot, Piece):
            self.active_pieces.remove((spot.team, spot))
        self.board[from_r][from_c] = self.empty
        self.board[to_r][to_c] = piece

        piece.pos = (to_r, to_c)

    def get_valid_moves(self, row, col):
        piece = self.board[row][col]
        if piece is None:
            return []  # No piece at that position
        return piece.valid_moves(self.board)

    def display_board(self):
        columns = 'abcdefgh'
        size = 8
        horizontal_line = '  +' + ('---+' * size)

        console.print('    ' + '   '.join(columns))  # Top column labels

        for row in range(size):
            console.print(horizontal_line)
            row_cells = []
            for col in range(size):
                piece = self.board[row][col]
                pos = (row, col)
                if piece is None:
                    if (row + col) % 2 == 0:
                        cell = "   "
                    else:
                        cell = "[dim] . [/]"
                else:
                    color = "white" if piece.team == "White" else "bright_red"
                    cell = f"[bold {color}] {piece.piece_symbol} [/]"
                row_cells.append(cell)

            console.print(f"{size - row} |" + "|".join(row_cells) + f"| {size - row}")

        console.print(horizontal_line)
        console.print('    ' + '   '.join(columns))  # Bottom column labels

    def check_pieces(self, piece_name, pos):
        pieces_able_to_move = []
        for team, piece in self.active_pieces:
            if team != self.team:
                continue

            if piece.piece != piece_name:
                continue

            valid_moves = piece.valid_moves(self.board)

            if pos in valid_moves:
                pieces_able_to_move.append(piece.pos)

        if len(pieces_able_to_move) == 1:
            r, c = pieces_able_to_move[0]
            t_r, t_c = pos
            self.move_piece(r, c, t_r, t_c)

    def copy_board(self, board):
        from copy import deepcopy
        return deepcopy(board)

    def copy_pieces(self, pieces):
        from copy import deepcopy
        return deepcopy(pieces)

    def get_piece_copy(self, piece, piece_list):
        for team, p in piece_list:
            if p.piece == piece.piece and p.pos == piece.pos and team == piece.team:
                return p

    def check_checkmate(self, board, active_pieces, king_team):
        # Find the king
        king = next(piece for team, piece in active_pieces if piece.piece == "King" and team == king_team)
        
        # First confirm the king is actually in check
        in_check = self.check_if_king_checked(board, active_pieces, king_team)
        if not in_check:
            return False  # Not in check, so cannot be checkmate

        # Try every possible move for every piece on this team
        for team, piece in active_pieces:
            if team != king_team:
                continue

            valid_moves = piece.valid_moves(board)

            for move in valid_moves:
                # Deep copy the board and pieces
                new_board = self.copy_board(board)
                new_pieces = self.copy_pieces(active_pieces)

                # Apply move in the cloned board
                temp_piece = self.get_piece_copy(piece, new_pieces)
                original_pos = temp_piece.pos
                temp_piece.pos = move
                new_board[original_pos[0]][original_pos[1]] = None
                new_board[move[0]][move[1]] = temp_piece

                # Remove captured piece if any
                new_pieces = [(t, p) for t, p in new_pieces if p.pos != move or t == king_team]

                # Check again
                if not self.check_if_king_checked(new_board, new_pieces, king_team):
                    return False  # Found a move that stops the check

        return True  # No move can stop the check ⇒ checkmate

    def check_if_king_checked(self):
        pieces_checking = []
        king_pos = [piece.pos for _, piece in self.active_pieces if piece.piece == 'King' and piece.team != self.team][0]
        r, c = king_pos
        king_team = self.board[r][c]

        for team, piece in self.active_pieces:
            if team == self.team:
                continue

            valid_moves = piece.valid_moves(self.board)

            if king_pos in valid_moves:
                pieces_checking.append((piece.piece, piece.pos))

        checked = False
        check_mate = False

        if pieces_checking:
            checked = True
            check_mate = self.check_checkmate(self.board, self.active_pieces, king_team.team)
    
        if check_mate:
            return check_mate, "Check-Mate"

        return checked, "Check"

    def play(self):
        self.playing = True
        while self.playing:
            cc()
            black_team, white_team = self.ai.evaluate(self.active_pieces)
            if self.team == 'White':
                print(f"Your Piece Score: {white_team} | AI Piece Score: {black_team}")
            else:
                print(f"AI Piece Score: {white_team} | Your Piece Score: {black_team}")
            self.display_board()
            if self.turn == 'Player':
                piece_to_check = self.moves.parse_input()
                if piece_to_check == True:
                    self.playing = False
                    continue

                piece, pos = piece_to_check
                self.check_pieces(piece, pos)
                self.turn = 'AI'
            
            else:
                f_pos, t_pos = self.ai.get_possible_moves(self.board, self.active_pieces)
                f_r, f_c = f_pos
                t_r, t_c = t_pos
                self.move_piece(f_r, f_c, t_r, t_c)
                self.turn = 'Player'
 
            check, tp = self.check_if_king_checked()

            if tp == 'Check-Mate':
                self.playing = False
                self.game_end()

    # -------------------------------------------------- Chess Tutorial Part --------------------------------------------------
    def handle_highlight_moves(self):
        while True:
            cc()
            self.display_practice_board()
            user_input = input("Select a position, or type exit: ").strip().lower()

            if len(user_input) == 2 and user_input[0] in 'abcdefgh' and user_input[1] in '12345678':
                cc()
                col = 'abcdefgh'.index(user_input[0])
                row = 8 - int(user_input[1])
                moves = self.get_valid_moves(row, col)
                self.display_practice_board(selected_pos=(row, col), highlighted_moves=moves)
                input('Press enter to continue.')

            elif user_input == 'exit':
                break

            else:
                print("Not a valid position.")
                input("Press enter to continue.")
    
    def display_practice_board(self, selected_pos = None, highlighted_moves = None):
        columns = 'abcdefgh'
        size = 8
        horizontal_line = '  +' + ('---+' * size)

        console.print('    ' + '   '.join(columns))  # Top column labels

        for row in range(size):
            console.print(horizontal_line)
            row_cells = []
            for col in range(size):
                piece = self.board[row][col]
                pos = (row, col)

                if pos == selected_pos:
                    if piece:
                        color = "white" if piece.team == "White" else "bright_red"
                        cell = f"[bold {color}][{piece.piece_symbol}][/]"
                    else:
                        cell = "   "
                elif highlighted_moves and pos in highlighted_moves:
                    cell = "[bold bright_white] # [/]"
                else:
                    if piece is None:
                        if (row + col) % 2 == 0:
                            cell = "   "
                        else:
                            cell = "[dim] . [/]"
                    else:
                        color = "white" if piece.team == "White" else "bright_red"
                        cell = f"[bold {color}] {piece.piece_symbol} [/]"
                row_cells.append(cell)

            console.print(f"{size - row} |" + "|".join(row_cells) + f"| {size - row}")

        console.print(horizontal_line)
        console.print('    ' + '   '.join(columns))

    def help_on_movement(self):
        pieces = ['Pawn', 'Bishop', 'Knight', 'Rook', 'Queen', 'King']

    def tutorial(self):
        run = True
        options = ["See a piece's moves", 'How to move a Piece', "Exit"]
        while run:
            cc()
            for i, opt in enumerate(options, 1):
                if i == len(options):
                    print(opt)
                else:
                    print(opt, end=' | ')

            user_input = input("Select an option: ").strip().title()
            
            if user_input == 'Exit' or user_input == 'E' or user_input.startswith('Exit'):
                run = False

            elif user_input == "See A Piece's Moves" or user_input == 'See' or user_input.startswith("See"):
                self.handle_highlight_moves()
            
            elif user_input == "How To Move A Piece" or user_input == 'How' or user_input.startswith("How"):
                self.help_on_movement()
            
            else:
                print("Not an option.")
                input("Press enter to continue.")

    # -------------------------------------------------- Main Part to load chess ----------------------------------------------
    def main(self):
        options = ['Play', 'Tutorial', 'Quit']

        while self.running:
            cc()
            for i, opt in enumerate(options, 1):
                if i == len(options):
                    print(opt)
                else:
                    print(opt, end=' | ')

            user_input = input("Select an option: ").strip().title()

            
            if user_input == 'Play' or user_input.startswith("Pl"):
                self.play()

            elif user_input == 'Tutorial' or user_input.startswith("Tut"):
                self.tutorial()

            elif user_input == 'Quit' or user_input.startswith("Q"):
                self.running = False

            else:
                print("Not an option.")
                input("Press enter to continue.")
        
        cc()
