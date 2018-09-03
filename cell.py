import tkinter
import random
import maze
import mouse
class Cell(object):
    def __init__(self, weight=-1, x=-1, y=-1, is_not_travellable=-1, travelled=-1, first_travelled = -1, traced=-1):
        self.weight=weight
        self.x=x
        self.y=y
        self.is_not_travellable=is_not_travellable
        self.travelled = travelled
        self.first_travelled = first_travelled
        self.traced = traced
        self.storage = []
        for i in range (30):
            a_row = []
            for j in range (30):
                a_row.append(-1)
            self.storage.append(a_row)



    def __str__(self):
        #return f'({self.x},{self.y},{self.weight} )'
        return "{:10.5f} ".format(self.weight)

    def get_weight(self):
        return self.weight

    def set_weight(self, weight):
        self.weight = weight

    def serialize(self,row,col):
        return f"{row},{col},{self.x},{self.y},{self.is_no_travellable}"

    def deserialize(self,str):
        parts = str.split(",")
        self.x = float(parts[2])
        self.y = float(parts[3])
        self.is_not_travellable = (parts[4] == 'True')
        return int(parts[0]),int(parts[1])

#    CELL_WIDTH = 20 # square width
#    DEFAULT_WEIGHT =0.1  # default weight
#    WALKABLE_CELL_COLOR = "gray"
#    BLOCKED_CELL_COLOR = "white"