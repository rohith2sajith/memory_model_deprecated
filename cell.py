import tkinter
import random
import maze
import mouse
class Cell(object):
    def __init__(self, weight, x, y, is_travellable, travelled):
        self.weight=weight
        self.x=x
        self.y=y
        self.is_travellable=is_travellable
        self.travelled = travelled

    def __str__(self):
        #return f'({self.x},{self.y},{self.weight} )'
        return "{:8.4f} ".format(self.weight)

    def get_weight(self):
        return self.weight

    def set_weight(self, weight):
        self.weight = weight

    CELL_WIDTH = 20 # square width
    DEFAULT_WEIGHT =0.1  # default weight
    WALKABLE_CELL_COLOR = "gray"
    BLOCKED_CELL_COLOR = "white"