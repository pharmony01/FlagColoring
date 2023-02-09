class Tile:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        
    # Color representation of the tile
    def __repr__(self):
        return str(self.color)