import numpy as np


def step(Field):
    '''
    Field - class of field
    
    Method generate new field by basics rules
    '''
    pole = Field.cells.copy()
    for x in range(1, pole.size_x - 1, 1): #FixMe Now programm doesn't work with borders
        for y in range(1, pole.size_y - 1, 1):
            if pole[x][y].fill:
                neighbors = 0
                if pole[x + 1][y].fill:
                    neighbors += 1
                if pole[x - 1][y].fill:
                    neighbors += 1
                if pole[x][y + 1].fill:
                    neighbors += 1
                if pole[x][y - 1].fill:
                    neighbors += 1
                if neighbors == 1 or neighbors == 4:
                    pole[x][y].fill = False
            else:
                neighbors = 0
                if pole[x + 1][y].fill:
                    neighbors += 1
                if pole[x - 1][y].fill:
                    neighbors += 1
                if pole[x][y + 1].fill:
                    neighbors += 1
                if pole[x][y - 1].fill:
                    neighbors += 1
                if neighbors == 3:
                    pole[x][y].fill = True
    Field.cells = pole.copy()
            
                
        
            