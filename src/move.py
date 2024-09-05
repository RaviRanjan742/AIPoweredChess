import chess

class Move:
    def __init__(self, initial, final):
        self.initial = initial
        self.final = final

    def __str__(self):
        s = ''
        s += f'({self.initial.col},{self.initial.row})'
        s += f'->({self.final.col},{self.final.row})'
        return s

    def __eq__(self, other):
        return self.initial == other.initial and self.final == other.final

    def to_chess_move(self):
        # Convert the move to chess.Move format
        # Assuming your board uses 0-based indexing
        # and the chess library uses 1-based indexing
        from_square = chr(self.initial.col + 97) + str(8 - self.initial.row)
        to_square = chr(self.final.col + 97) + str(8 - self.final.row)
        return chess.Move.from_uci(from_square + to_square)