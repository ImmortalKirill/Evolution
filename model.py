import numpy as np


def step(Field):
    '''
    Field - class of Field
    
    Method generate new field by basics rules
    '''
    pole = Field.cells.copy()
    for x in range(1, Field.size_x - 1, 1): # FixMe Now program doesn't work with borders
        for y in range(1, Field.size_y - 1, 1):
            # counting number of neighbors
            neighbors = 0
            if pole[x + 1][y].live:
                neighbors += 1
            if pole[x - 1][y].live:
                neighbors += 1
            if pole[x][y + 1].live:
                neighbors += 1
            if pole[x][y - 1].live:
                neighbors += 1
            # checking future for cell
            if pole[x][y].live > 0:
                if neighbors < 2 or neighbors == 4:
                    pole[x][y].live -= 1
            else:
                if neighbors == 3:
                    pole[x][y].live += 1
    Field.cells = pole.copy()

def change_scale(field, par):
    """changes scale of field, increases it if par = 1, decreases it if par = -1"""
    change_step = 10
    field.scale += par*change_step
            
            
if __name__ == "__main__":
    print("This module is not for direct call!")

        
            