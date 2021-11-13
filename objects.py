class Cell():
    """ class of one cell on a Field"""
    def __init__():
        live = self.live = 1
        x = self.x = 0
        y = self.y = 0
    
        
    def new_cell(x0, y0):
        x = self.x = x0
        y = self.y = y0
        


class Field():
    """ class Field, consists of cells"""
    def __init__():
        cells = [[0 for i in range(y)] for i in range(x)]        
        x_center = self.x_center = x / 2
        y_center = self.y_center = y / 2
        scale = self.scale = 1
        
        
    def new_field(x, y):
        for i in range(x):
            for l in range(y):
                cells[x][y] = Cell()
                cells[x][y].new_cell(x, y)        

        
if __name__ == "__main__":
    print("This module is not for direct call!")