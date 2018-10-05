import tkinter
import config as config
import cell
import maze
from tkinter import filedialog
import os
from tkinter import IntVar

class MazeBuilder:
    DEFAULT_WEIGHT = 0.1  # default weight
    DAMAGE_FILL_COLORS = ["coral1","coral2","coral3","tomato2","tomato3","tomato4","orangered2","orangered3","red4","black"]
    def __init__(self):
        self.my_maze = maze.Maze(None)
        self.my_maze.blank_board()
        self.my_maze.setup_default_maze()

    def setup_ui_control(self,my_frame):
        tkinter.Button(my_frame, text='SAVE', width=20, command=self.save).grid(row=0, column=0)
        tkinter.Button(my_frame, text='LOAD', width=20, command=self.load).grid(row=0, column=1)
        tkinter.Label(my_frame, text='GRID SIZE', width=10).grid(sticky="W", row=1, column=0)
        tkinter.Entry(my_frame, width=10, textvar=self.grid_size_var).grid(sticky="W", row=1, column=1)
        tkinter.Button(my_frame, text='APPLY', width=20, command=self.apply_config_handler).grid(sticky="W", row=1, column=2)

    def setup_ui_canvas(self,my_frame):
        tkinter.Canvas(my_frame,
                       width=config.CELL_WIDTH ,
                       height=config.CELL_WIDTH * config.NUMBER_OF_CELLS).grid(sticky="W", row=0, column=0)

        self.canvas = tkinter.Canvas(my_frame,
                                width=config.CELL_WIDTH * config.NUMBER_OF_CELLS,
                                height=config.CELL_WIDTH * config.NUMBER_OF_CELLS)
        self.canvas.grid(sticky="W", row=0, column=1)
        tkinter.Canvas(my_frame,
                              width=config.CELL_WIDTH,
                              height=config.CELL_WIDTH * config.NUMBER_OF_CELLS).grid(sticky="W", row=0, column=2)

    def draw_board(self):
        self.root = tkinter.Tk()  # start the gui engine

        self.grid_size_var = IntVar()
        self.grid_size_var.set(config.NUMBER_OF_CELLS)

        self.top_frame = tkinter.Frame(self.root)
        self.top_frame.grid(row=0, column=0)

        self.setup_ui_control(self.top_frame)

        canvas_frame = tkinter.Frame(self.root)
        canvas_frame.grid(row=1, column=0)
        self.setup_ui_canvas(canvas_frame)

        #self.canvas = tkinter.Canvas(canvas_frame,
        #                        width=config.CELL_WIDTH * config.NUMBER_OF_CELLS,
        #                        height=config.CELL_WIDTH * config.NUMBER_OF_CELLS)
        #left = tkinter.Canvas(canvas_frame,
        #               width=config.CELL_WIDTH ,
        #               height=config.CELL_WIDTH * config.NUMBER_OF_CELLS)
        #right = tkinter.Canvas(canvas_frame,
        #                      width=config.CELL_WIDTH,
        #                      height=config.CELL_WIDTH * config.NUMBER_OF_CELLS)


        # pack mean you add show the canvas. By default it will not show
        #left.grid(row=2,column=0)
        #self.canvas.grid(row=2, column=1)
        #right.grid(row=2, column=2)
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
        self.update_ui(self.my_maze.board)

        self.root.mainloop()

    def apply_config_handler(self):
        print("Apply config")

        if config.NUMBER_OF_CELLS != int(self.grid_size_var.get()):
            board = MazeBuilder.load_board("default")
            self.my_maze.reinitialize(board)
            self.resize()
    def to_tag(self,row,col):
        return f"{row}-{col}"

    def from_tag(self,tag):
        parts = tag.split("-")
        return int(parts[0]), int(parts[1])

    def toggle_fill_color(self,current_color):
        if current_color == config.WALKABLE_CELL_COLOR:
            return  config.BLOCKED_CELL_COLOR
        return config.WALKABLE_CELL_COLOR
    @staticmethod
    def get_fill_color(is_travelable):
        if is_travelable:
            return config.BLOCKED_CELL_COLOR
        return config.WALKABLE_CELL_COLOR

    @staticmethod
    def get_damage_fill_color(index):
        return MazeBuilder.DAMAGE_FILL_COLORS[index]

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
        file_path = filedialog.asksaveasfilename()
        self.my_maze = maze.Maze(None)
        board = self.my_maze.blank_board()

        for s in self.canvas.find_all():
            current_fill = self.canvas.itemcget(s, 'fill')
            row,col = self.from_tag(self.canvas.gettags(s)[0])
            board[row][col].is_not_travellable = self.is_shaded(current_fill)

            self.my_maze.save(file_path)
        # test
        self.clear_board()
        self.update_ui(board)

    def update_ui(self,board):
        for i in range(config.NUMBER_OF_CELLS):
            for j in range(config.NUMBER_OF_CELLS):
                s = self.canvas.find_withtag(self.to_tag(i,j))[0]
                self.canvas.itemconfig(s, fill=self.get_fill_color(board[i][j].is_not_travellable))

    def load_from_file(self,filename):
        #self.my_maze = maze.Maze(None)
        #self.my_maze.load(filename)
        #self.load_from_board(self.my_maze.board)
        board = self.load_board(filename)
        self.my_maze = maze.Maze(None)
        self.my_maze.board = board
        self.update_ui(board)

    def load(self):
        print("loading")
        file_path = filedialog.askopenfilename()
        self.load_from_file(file_path)

    @staticmethod
    def blank_board():
        """

        :return:
        """
        x = 0
        y = 0
        board = []
        for row in range(config.NUMBER_OF_CELLS):
            x = 0
            a_row = []
            for col in range(config.NUMBER_OF_CELLS):
                is_not_travellable = False
                travelled = -1
                first_travelled = -1
                traced = False
                a_row.append(cell.Cell(MazeBuilder.DEFAULT_WEIGHT, x, y, is_not_travellable, travelled, first_travelled, traced))
                x += 1
            y += 1
            board.append(a_row)
        return board

    @staticmethod
    def load_board(filename):
        board = MazeBuilder.blank_board()
        filename = f"mazes/{filename}_{config.NUMBER_OF_CELLS}x{config.NUMBER_OF_CELLS}.mze"
        if os.path.isfile(filename):
            with open(filename, 'r') as maz_file:
                for line in maz_file:
                    line = line.strip("\n")
                    my_cell = cell.Cell()
                    row, col = my_cell.deserialize(line)
                    board[row][col] = my_cell
        return board


def main():
    maz_builder = MazeBuilder()
    maz_builder.draw_board()

if __name__ == '__main__':
    main()