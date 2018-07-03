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
    return max_x_coord() - CELL_WIDTH  # 580
def exit_cell_x2():
    return max_x_coord()  # 600

def exit_cell_y1():
    return 0
def exit_cell_y2():
    return CELL_WIDTH  # 20

def p(msg):
    if not debug_print:
        return
    print(msg,end='')
def pl(*msg):
    if not debug_print:
        return
    p(msg)
    print()

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
    return x, y
