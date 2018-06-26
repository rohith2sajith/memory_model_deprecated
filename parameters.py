CELL_WIDTH = 20 # square width
DEFAULT_WEIGHT =0.1  # default weight
WALKABLE_CELL_COLOR = "gray"
BLOCKED_CELL_COLOR = "white"
NUMBER_OF_CELLS=30
MOUSE_RADIUS=8
MOUSE_FILL_COLOR="red"
SUGGESTED_MOUSE_FILL_COLOR="yellow"
PATH_LINE_COLOR="green"
DEFAULT_NUM_LEARNING_STEPS=1000

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