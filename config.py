import random
from sympy.geometry import *
from datetime import datetime

CELL_WIDTH = 20  # square width
DEFAULT_WEIGHT = 0.1  # default weight
WALKABLE_CELL_COLOR = "white"
BLOCKED_CELL_COLOR = "gray"
NUMBER_OF_CELLS = 30
MOUSE_RADIUS = 8
MOUSE_FILL_COLOR = "red"
SUGGESTED_MOUSE_FILL_COLOR = "yellow"
PATH_LINE_COLOR = "green"
num_learning_steps = 1000
debug_print=True

def max_y_coord():
    return CELL_WIDTH * NUMBER_OF_CELLS # 600

def max_x_coord():
    return CELL_WIDTH * NUMBER_OF_CELLS # 600

def exit_cell_x1():
    return 200
def exit_cell_x2():
    return 220

def exit_cell_y1():
    return 300
def exit_cell_y2():
    return 320

def p(msg):
    if not debug_print:
        return
    print(msg,end='')
def pl(*msg):
    if not debug_print:
        return
    p(msg)
    print()
def is_in_range(x,y,line):
    x1 = line[0][0]
    y1 = line[0][1]
    x2 = line[1][0]
    y2 = line[1][1]
    if x1 != x and x2 != x:
        if min(x1,x2,x) == x or max(x1,x2,x) == x:
            return False
    if y1 != y and y2 != y:
        if min(y1,y2,y) == y or max(y1,y2,y) == y:
            return False
    return True

def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1]) #Typo was here

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
       return None,None

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    if not is_in_range(x,y,line1):
        return None,None
    if not is_in_range(x,y,line2):
        return None,None

    return x, y

def main():
    for i in range(100):

        line1 = [[100* random.random(),100* random.random()],[100* random.random(),100* random.random()]]
        line2 = [[100* random.random(),100* random.random()],[100* random.random(),100* random.random()]]
        p11 = (line1[0][0],line1[0][1])
        p12 = (line1[1][0],line1[1][1])
        p21 = (line2[0][0], line2[0][1])
        p22 = (line2[1][0], line2[1][1])
        t1 = datetime.now().microsecond
        inter_value = intersection(Segment2D(p11,p12),Segment2D(p21,p22))
        t2 = datetime.now().microsecond
        t3 = datetime.now().microsecond
        x2, y2 = line_intersection(line1, line2)
        t4 = datetime.now().microsecond
        if inter_value:
            x1= float(inter_value[0].x)
            y1 = float(inter_value[0].y)
            print(x1,y1,x2,y2,end=' ')
            print(x2,y2, end=' ')
        else:
            print('#################',x2, y2)
        print("TIME ",(t2-t1),(t3-t4))