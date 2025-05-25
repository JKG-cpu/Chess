import os, time
from rich.console import Console
console = Console()

from pieces import Pawn, Knight, Bishop, Rook, Queen, King

def cc():
    os.system('cls' if os.name == 'nt' else 'clear')

class Board:
    def __init__(self):
        self.starting_positions = {
            'White': {
                'Pawn':    [(6, i) for i in range(8)],
                'Rook':    [(7, 0), (7, 7)],
                'Knight':  [(7, 1), (7, 6)],
                'Bishop':  [(7, 2), (7, 5)],
                'Queen':   [(3, 3)],
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
        }

        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.empty = None
        self.active_pieces = []
        self.generate_board()

        self.team = 'White'

        self.running = True

    def handle_move_piece(self):
        run = True
        while run:
            cc()
            self.display_board()
            user_input = input('Enter a piece to select: ').strip().lower()

            if len(user_input) == 2 and user_input[0] in 'abcdefgh' and user_input[1] in '12345678':
                from_r = 8 - int(user_input[1])
                from_c = 'abcdefgh'.index(user_input[0])
                selection = self.board[from_r][from_c]
                if selection.team != self.team:
                    print("That is not your piece.")
                    input("Press enter to continue.")
                else:
                    valid_moves = self.get_valid_moves(from_r, from_c)

                    while True and valid_moves:
                        user_inp = input("Enter a place to go: ").strip().lower()
                        if len(user_inp) == 2 and user_inp[0] in 'abcdefgh' and user_inp[1] in '12345678':
                            to_r = 8 - int(user_inp[1])
                            to_c = 'abcdefgh'.index(user_inp[0])
                            pos = (to_r, to_c)

                            if pos in valid_moves:
                                self.move_piece(from_r, from_c, to_r, to_c)
                                return
                            
                            else:
                                print('Not a valid place to move.')
                            
                            time.sleep(0.2)
                            
                        else:
                            print("Not a valid move.")

                    if not valid_moves:
                        input("No Valid moves for that piece, press enter to continue.")

            else:
                print("Not an option.")
                input("Press enter to continue.")
                run = False

    def move_piece(self, from_r, from_c, to_r, to_c):
        piece = self.board[from_r][from_c]
        self.board[from_r][from_c] = self.empty
        self.board[to_r][to_c] = piece

        piece.pos = (to_r, to_c)

    def get_valid_moves(self, row, col):
        piece = self.board[row][col]
        if piece is None:
            return []  # No piece at that position
        return piece.valid_moves(self.board)

    def create_peice(self, type, team, row, col):
        # Knight, Bishop, Rook, Queen, King
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
    
        piece = types[type](team, row, col)
        self.active_pieces.append((team, piece))
        self.board[row][col] = piece

    def generate_board(self):
        for team in self.starting_positions:
            for piece in self.starting_positions[team]:
                for row, col in self.starting_positions[team][piece]:
                    self.create_peice(piece, team, row, col)

    def display_board(self, selected_pos=None, highlighted_moves=None):
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
        console.print('    ' + '   '.join(columns))  # Bottom column labels

    def handle_highlight_moves(self):
        while True:
            cc()
            self.display_board()
            user_input = input("Select a position, or type exit: ").strip().lower()

            if len(user_input) == 2 and user_input[0] in 'abcdefgh' and user_input[1] in '12345678':
                cc()
                col = 'abcdefgh'.index(user_input[0])
                row = 8 - int(user_input[1])
                moves = self.get_valid_moves(row, col)
                self.display_board(selected_pos=(row, col), highlighted_moves=moves)
                input('Press enter to continue.')

            elif user_input == 'exit':
                break

            else:
                print("Not a valid position.")
                input("Press enter to continue.")

    def main(self):
        while self.running:
            cc()
            self.display_board()
            user_input = input("Would you like to move a piece (m), or see valid moves for a piece (vm), or quit: ").strip().lower()
            
            if user_input == 'vm':
                self.handle_highlight_moves()

            elif user_input == 'm':
                self.handle_move_piece()

            elif user_input == 'quit':
                self.running = False

            else:
                print("Not a valid position.")

if __name__ == "__main__":
    board = Board()
    board.main()
    cc()
