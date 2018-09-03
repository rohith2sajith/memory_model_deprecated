import cell
import mouse
import maze
import rundata
import config as config
import tkinter
import numpy as np
from sympy import *
from sympy.geometry import *
from sympy.core.numbers import *
import copy
from tkinter import filedialog
from tkinter import IntVar
from datetime import datetime
class RunData(object):

    def __init__(self):
        self.run_id = 0
        self.num_directions = 0
        self.num_traps = 0
        self.search_length = 0
        self.learning_length = 0
        self.time = 0
        self.num_squares = 1
        self.displacements = []
    @staticmethod
    def report_heading():
        return "num_directions,num_traps,search_length,learning_length,time,num_squares,index,displacement"

    def __str__(self):
        str = ""
        cr=""
        i =0
        for d in self.displacements:
            str = f"{str}{cr}{self.num_directions},{self.num_traps},{self.search_length},{self.learning_length},{self.time},{self.num_squares},{i},{d}"
            cr="\n"
            i+=1
        return  str
    def shorter_str(self):
        return f"{self.num_directions},{self.num_traps},{self.search_length},{self.learning_length},{self.time},{self.num_squares}"



