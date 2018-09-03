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
LOG_LEVEL_DEBUG=3
LOG_LEVEL_INFO=2
LOG_LEVEL_NONE=1
log_level = LOG_LEVEL_INFO
DAMAGE_MODE_SINGLE_CELL=0
DAMAGE_MODE_ADJ_CELL=1
DAMAGE_MODE_SPREAD_CELL=2



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

def d(msg):
    if log_level<LOG_LEVEL_DEBUG:
        return
    print(msg,end='')
def i(msg):
    if  log_level < LOG_LEVEL_INFO:
        return
    print(msg,end='')

def dl(msg):
    if log_level<LOG_LEVEL_DEBUG:
        return
    print(msg)
def il(msg):
    if log_level < LOG_LEVEL_INFO:
        return
    print(msg)

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

def equation_of_line(line):
    x1 = line[0][0]
    y1 = line[0][1]
    x2 = line[1][0]
    y2 = line[1][1]

    infinite_slope = x1 == x2
    m = 0
    if not infinite_slope:
        m = (y2-y1)/(x2-x1)
        b = y1 - m*x1
        return (m,b)
    return (None,x1)

def is_in_range_vertical(y1,y2,y):
    return y>= min(y1,y2) and y<= max(y1,y2)

def line_intersection_same_slope(y1,y2,y3,y4):
    a1 = min(y1,y2)
    a2 = max(y1,y2)
    b1 = min(y2,y3)
    b2 = max(y2,y3)
    # line 1 is a1-a2 a2>=a1
    # line 2 is b1-b2 b2>=b1

    if a1 == b1 and a2 == b2: # both lines are same same l
        return a1,a2
    if is_in_range_vertical(a1,a2,b1):
       # b1 is point
        if is_in_range_vertical(a1,a2,b2):
            # b2 is also point
            return b1,b2
        else:
            return b1,a2
    elif is_in_range_vertical(a1,a2,b2):
        return a1,b2
    else:
        return None,None

def line_intersection(line1, line2):
    # find slope of fist line
    m1, b1 = equation_of_line(line1)
    m2, b2 = equation_of_line(line2)
    if m1 != None and m2 != None:
        # None of the lines are parallel to y-axis
        if m1 != m2:
            # sliopes are not equal
            x = (b2-b1)/(m1-m2)
            y = m1 * x + b1
        else:
            # slopes are equal and not parallel to y-axis
            # two case
            if b1 == b2:
                # y intercep are also  equal
                # two cases prallel to x axis
                x1, x2 = line_intersection_same_slope(line1[0][0], line1[1][0], line2[0][0], line2[1][0])
                x = x1
                y1, y2 = line_intersection_same_slope(line1[0][1], line1[1][1], line2[0][1], line2[1][1])
                y = y1
                # other wise
            else:
                # slopes are equal but differet y intercepts
                # so no intersection
                return None,None
    elif m1 == None and m2 == None:
        # Both lines are parallel to y axis
        x = line1[0][0]
        x1,x2 = line_intersection_same_slope(line1[0][0], line1[1][0], line2[0][0], line2[1][0])
        x = x1
        y1, y2 = line_intersection_same_slope(line1[0][1], line1[1][1], line2[0][1], line2[1][1])
        y = y1
    elif m1 == None:
        # line one is parallel to y -axis
        if b1 != None:
            x = b1
            y = m2 * x + b2
        else:
            return None,None
    else: # m2 == None:
        # line2 is parallel y-axis
        if b2 != None:
            x = b2
            y = m1 * x + b1
        else:
            return None,None

    if is_in_range(x, y,line1) and is_in_range(x, y,line2):
        return x, y
    else:
        return None, None


def line_intersection_old(line1, line2):
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