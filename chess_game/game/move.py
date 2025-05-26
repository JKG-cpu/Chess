import time
import os

from .pieces import *

def cc():
    os.system('cls' if os.name == 'nt' else 'clear')

class Moves:
    def __init__(self, player_team):
        self.player_team = player_team
        self.turn = 'Player'
        self.pieces_nicknames = {
            'B': "Bishop",
            'N': "Knight",
            'R': 'Rook',
            'Q': "Queen",
            'K': "King"
        }
        self.quit = False

    def parse_input(self):
        while True:
            move = input('Enter Position to play, or type quit: ').strip().title()

            if move == 'Quit':
                self.quit = True
                return self.quit  
            
            if len(move) == 2:
                piece_to_move = 'Pawn'
                if move[0].lower() in 'abcdefgh' and move[1] in '12345678':
                    col = 'abcdefgh'.index(move[0].lower())
                    row = 8 - int(move[1])
                    pos = (row, col)
                    return (piece_to_move, pos)
                else:
                    print("Not a valid position.")
                    input("")

            elif len(move) == 3:
                if move[0] in self.pieces_nicknames:
                    piece_to_move = self.pieces_nicknames[move[0]]
                    if move[1] in 'abcdefgh' and move[2] in '12345678':
                        col = 'abcdefgh'.index(move[1])
                        row = 8 - int(move[2])
                        pos = (row, col)
                        return (piece_to_move, pos)
                    else:
                        print("Not a valid position.")
                else:
                    print("Not a valid piece")
                    input("Press enter to continue.")

            else:
                print("Not a valid move")
                input("Press enter to continue.")

    def main(self):
        if self.turn == 'Player':
            self.parse_input()
            return self.quit  # Return quit status
        
        elif self.turn == 'AI':
            self.turn = 'Player'  # Fixed assignment
            return False
