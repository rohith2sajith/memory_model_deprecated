import tkinter
import random
import maze

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
def draw_board(board):
    root = tkinter.Tk()  # start the gui engine
    # create canvas
    # you can draw rectacngle , lines points etc in a canvas

    canvas = tkinter.Canvas(root,
                            width=CELL_WIDTH * 30,
                            height=CELL_WIDTH * 30)
    # pack mean you add show the canvas. By default it will not show
    canvas.pack()
    # now create rectangle
    for i in range(30):
        for j in range(30):
            cell = board[i][j]
            # rectangle need (x1,y1) and x2,y2)
            if cell.is_travellable:
                fill_color = WALKABLE_CELL_COLOR
            else:
                fill_color = BLOCKED_CELL_COLOR
            box = canvas.create_rectangle(CELL_WIDTH * j,
                                          CELL_WIDTH * i,
                                          CELL_WIDTH * (j + 1),
                                          CELL_WIDTH * (i + 1),
                                          fill=fill_color)
    # you need to call this so that the GUI start running
    root.mainloop()
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




if __name__ == '__main__':
    main()
