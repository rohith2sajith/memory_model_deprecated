import tkinter
import config as config
import cell
import maze
from tkinter import filedialog

class MazeBuilder:
    def __init__(self):
        self.my_maze = maze.Maze([])
        self.my_maze.blank_board()
        self.my_maze.setup_default_maze()

    def draw_board(self):
        self.root = tkinter.Tk()  # start the gui engine

        ## TOP CONTROL FRAME
        self.top_frame = tkinter.Frame(self.root)

        self.learning_button = tkinter.Button(self.top_frame, text='SAVE',
                                              width=20,
                                              command=self.save)

        self.path_button = tkinter.Button(self.top_frame, text='LOAD',
                                          width=20,
                                          command=self.load)
        self.learning_button.grid(row=0, column=0)
        self.path_button.grid(row=0, column=1)
        self.top_frame.grid(row=0, column=0)

        ## BOARD CANVAS
        canvas_frame = tkinter.Frame(self.root)
        self.canvas = tkinter.Canvas(canvas_frame,
                                width=config.CELL_WIDTH * config.NUMBER_OF_CELLS,
                                height=config.CELL_WIDTH * config.NUMBER_OF_CELLS)
        left = tkinter.Canvas(canvas_frame,
                       width=config.CELL_WIDTH ,
                       height=config.CELL_WIDTH * config.NUMBER_OF_CELLS)
        right = tkinter.Canvas(canvas_frame,
                              width=config.CELL_WIDTH,
                              height=config.CELL_WIDTH * config.NUMBER_OF_CELLS)

        canvas_frame.grid(row=1,column=0)
        # pack mean you add show the canvas. By default it will not show
        left.grid(row=1,column=0)
        self.canvas.grid(row=1, column=1)
        right.grid(row=1, column=2)
        self.canvas.bind("<Button-1>", self.on_clicked)

        for i in range(config.NUMBER_OF_CELLS):
            for j in range(config.NUMBER_OF_CELLS):
                # rectangle need (x1,y1) and x2,y2)
                fill_color = config.WALKABLE_CELL_COLOR
                box = self.canvas.create_rectangle(config.CELL_WIDTH * j,
                                                   config.CELL_WIDTH * i,
                                                   config.CELL_WIDTH * (j + 1),
                                                   config.CELL_WIDTH * (i + 1),
                                                   fill=fill_color,tags=self.to_tag(i,j))
        self.load_form_board(self.my_maze.board)

        self.root.mainloop()

    def to_tag(self,row,col):
        return f"{row}-{col}"

    def from_tag(self,tag):
        parts = tag.split("-")
        return int(parts[0]), int(parts[1])

    def toggle_fill_color(self,current_color):
        if current_color == config.WALKABLE_CELL_COLOR:
            return  config.BLOCKED_CELL_COLOR
        return config.WALKABLE_CELL_COLOR

    def get_fill_color(self,is_travelable):
        if is_travelable:
            return config.BLOCKED_CELL_COLOR
        return config.WALKABLE_CELL_COLOR

    def is_shaded(self,color):
        return color == config.BLOCKED_CELL_COLOR

    def clear_board(self):
        for s in self.canvas.find_all():
            self.canvas.itemconfig(s, fill=config.WALKABLE_CELL_COLOR)
        self.root.update()

    def on_clicked(self,e):
        shape = self.canvas.find_closest(e.x, e.y)
        current_fill = self.canvas.itemcget(shape, 'fill')

        self.canvas.itemconfig(shape, fill=self.toggle_fill_color(current_fill))

    def blank_board(self):
        x = 0
        y = 0
        board = []
        for i in range(config.NUMBER_OF_CELLS):
            a_row = []
            for j in range(config.NUMBER_OF_CELLS):
                a_row.append(cell.Cell(config.DEFAULT_WEIGHT, x, y, False, -1, False))
            board.append(a_row)
        return board

    def save(self):
        print('saving')
        file_path = filedialog.askopenfilename()
        self.my_maze = maze.Maze([])
        board = self.my_maze.blank_board()

        for s in self.canvas.find_all():
            current_fill = self.canvas.itemcget(s, 'fill')
            row,col = self.from_tag(self.canvas.gettags(s)[0])
            board[row][col].is_travellable = self.is_shaded(current_fill)

            self.my_maze.save(file_path)
        # test
        self.clear_board()
        self.load_form_board(board)

    def load_form_board(self,board):
        for i in range(config.NUMBER_OF_CELLS):
            for j in range(config.NUMBER_OF_CELLS):
                s = self.canvas.find_withtag(self.to_tag(i,j))[0]
                self.canvas.itemconfig(s, fill=self.get_fill_color(board[i][j].is_travellable))

    def load_from_file(self,filename):
        self.my_maze = maze.Maze([])
        self.my_maze.load(filename)
        self.load_form_board(self.my_maze.board)

    def load(self):
        print("loading")
        file_path = filedialog.askopenfilename()
        self.load_from_file(file_path)

def main():
    maz_builder = MazeBuilder()
    maz_builder.draw_board()

if __name__ == '__main__':
    main()