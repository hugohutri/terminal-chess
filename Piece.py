class Piece:
    def __init__(self, name, icon, color, position):
        self.name = name
        self.icon = icon
        self.color = color
        self.position = position
        self.moves = 0

    def did_move(self):
        self.moves += 1

    def get_moves(self):
        return self.moves