import tkinter
import random
import maze
import mouse
class Cell(object):
    def __init__(self, weight=-1, x=-1, y=-1, is_travellable=-1, travelled=-1, traced=-1):
        self.weight=weight
        self.x=x
        self.y=y
        self.is_travellable=is_travellable
        self.travelled = travelled
        self.traced = traced


    def __str__(self):
        #return f'({self.x},{self.y},{self.weight} )'
        return "{:8.4f} ".format(self.weight)

    def get_weight(self):
        return self.weight

    def set_weight(self, weight):
        self.weight = weight

    def serialize(self,row,col):
        return f"{row},{col},{self.x},{self.y},{self.is_travellable}"

    def deserialize(self,str):
        parts = str.split(",")
        self.x = float(parts[2])
        self.y = float(parts[3])
        self.is_travellable = (parts[4] == 'True')
        return int(parts[0]),int(parts[1])

#    CELL_WIDTH = 20 # square width
#    DEFAULT_WEIGHT =0.1  # default weight
#    WALKABLE_CELL_COLOR = "gray"
#    BLOCKED_CELL_COLOR = "white"