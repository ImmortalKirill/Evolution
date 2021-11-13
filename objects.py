class Cell(x0, y0):
    """ class of one cell on a Field"""
    def __init__():
        live = self.live = 1
        x = self.x = x0
        y = self.y = y0
        


class Field(x, y):
    """ class Field, consists of cells"""
    def __init__():
        cells = [[Cell(l, i) for i in range(y)] for l in range(x)]
        x_center = self.x_center = x / 2
        y_center = self.y_center = y / 2
        scale = self.scale = 1
