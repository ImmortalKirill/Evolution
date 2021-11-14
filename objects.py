class Cell():
    """ class of one cell on a Field"""
    def __init__(self):
        live = self.live = 1
        x = self.x = 0
        y = self.y = 0
    
        
    def new_cell(self, x0, y0):
        x = self.x = x0
        y = self.y = y0
        


class Field():
    """ class Field, consists of cells"""
    def __init__(self):
        cells = self.cells = [[]]        
        x_center = self.x_center = 0
        y_center = self.y_center = 0
        scale = self.scale = 50
        size_x = self.size_x = 0
        size_y = self.size_y = 0
        
        
    def new_field(self, x, y):
        """ creates new field with size x:y cells"""
        self.cells = [[0] * y for l in range(x)]
        for i in range(x):
            for l in range(y):
                self.cells[i][l] = Cell()
                self.cells[i][l].new_cell(i, l)  
        self.x_center = x / 2
        self.y_center = y / 2
        self.size_x = x
        self.size_y = y
    def change_cors(self, vector):
        """shift of center coordinates on vector(x, y)"""
        self.x_center += vector[0]
        self.y_center += vector[1]

        
if __name__ == "__main__":
    print("This module is not for direct call!")