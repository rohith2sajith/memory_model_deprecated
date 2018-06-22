import tkinter
import random
import maze
import mouse

class Cell(object):
    def __init__(self,weight,x,y, is_travellable):
        self.weight=weight
        self.x=x
        self.y=y
        self.is_travellable=is_travellable

    def __str__(self):
        return f'({self.x},{self.y} )'

    CELL_WIDTH = 20 # square width
    DEFAULT_WEIGHT =0.1  # default weight
    WALKABLE_CELL_COLOR = "gray"
    BLOCKED_CELL_COLOR = "white"
def main():
    x = 0
    y =0
    board = []
    for row in range(30):
        x = 0
        a_row = []
        for col in range(30):
            # print (f"x:{x} y:{y}")
            x +=CELL_WIDTH
            # for testing make the is_travelable random
            is_travelable = False

            a_row.append(Cell(DEFAULT_WEIGHT,x,y,is_travelable))
        y += CELL_WIDTH
        board.append(a_row)

    my_maze = maze.Maze(board)

    draw_board(my_maze.board)

    rat = mouse.Mouse(0,0,0,0,0)

    while rat.get_v() > rat.MIN:
        rat.set_a(rat.get_next_acceleration())
        rat.set_v(rat.get_next_velocity(rat.get_v(),rat.get_a(),rat.get_t()))
        rat.set_x(rat.get_next_coordinate(rat.get_x(),rat.get_y(),rat.get_v(),rat.get_t())[0])
        rat.set_y(rat.get_next_coordinate(rat.get_x(), rat.get_y(), rat.get_v(),rat.get_t())[1])


if __name__ == '__main__':
    main()
