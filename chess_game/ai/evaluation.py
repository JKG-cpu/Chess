class Evalution:
    def __init__(self):
        self.piece_values = {
            'Pawn': 1,
            'Knight': 3,
            'Bishop': 3,
            'Rook': 5,
            'Queen': 9,
            'King': 0
        }
        self.teams = ['Black', 'White']
        self.team1 = {'Team': 'Black', 'Score': 0}
        self.team2 = {'Team': "White", 'Score': 0}

    def evaluate(self, active_pieces):
        self.team1['Score'] = 0
        self.team2['Score'] = 0
        for team, piece in active_pieces:
            if team == self.team1['Team']:
                self.team1['Score'] += self.piece_values[piece.piece]
            else:
                self.team2['Score'] += self.piece_values[piece.piece]
        
        return self.team1['Score'], self.team2['Score']