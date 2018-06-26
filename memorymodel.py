import cell
import mouse
import maze
import config as config
import tkinter

class MemoryModel (object):
    CELL_WIDTH = 20 # square width
    DEFAULT_WEIGHT =0.1  # default weight
    WALKABLE_CELL_COLOR = "gray"
    BLOCKED_CELL_COLOR = "white"

    def draw_board(self):
        self.root = tkinter.Tk()  # start the gui engine
        self.top_frame = tkinter.Frame(self.root)
        self.top_frame.grid(row=0, column=0)

        self.learning_button = tkinter.Button(self.top_frame, text='START LEARNING',
                                        width=20,
                                        command=self.start_learning)

        self.path_button = tkinter.Button(self.top_frame, text='FIND PATH',
                                              width=20,
                                              command=self.find_path)
        self.iterations = tkinter.Entry (self.top_frame)
        self.apply_button = tkinter.Button(self.top_frame, text='APPLY',
                                          width=20,
                                          command=self.apply_config)
        label = tkinter.Label(self.top_frame, text='ITERATIONS',
                                           width=20)
        self.learning_button.grid(row=0, column=0)
        self.path_button.grid(row=0, column=1)
        label.grid(row=1, column=0)
        self.iterations.grid(row=1, column=1)
        self.apply_button.grid(row=1, column=2)


        # create canvas

        # you can draw rectangle , lines points etc in a canvas
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

        self.status = tkinter.Label(self.root, text="STATUS:")
        self.status.grid(row=2, column=0)

        # now create rectangle
        for i in range(config.NUMBER_OF_CELLS):
            for j in range(config.NUMBER_OF_CELLS):
                cell = self.board[i][j]
                # rectangle need (x1,y1) and x2,y2)
                if cell.is_travellable:
                    fill_color = self.WALKABLE_CELL_COLOR
                else:
                    fill_color = self.BLOCKED_CELL_COLOR
                box = self.canvas.create_rectangle(self.CELL_WIDTH * j,
                                              self.CELL_WIDTH * i,
                                              self.CELL_WIDTH * (j + 1),
                                              self.CELL_WIDTH * (i + 1),
                                              fill=fill_color)
        # you need to call this so that the GUI start running

        self.root.mainloop()
    def update_status(self,txt):
        self.status.configure(text=txt)

    def apply_config(self):
        print(self.iterations.get())
        config.num_learning_steps=int(self.iterations.get())

    def start_learning(self):
        self.move_mouse(self.rat)
        self.print_board()

    def find_path(self):
        self.canvas.delete("path")
        self.canvas.update()
        self.path(self.rat)
        self.print_board()

    def init_board(self):
        x = 0
        y = 0
        self.board = []
        for row in range(config.NUMBER_OF_CELLS):
            x = 0
            a_row = []
            for col in range(config.NUMBER_OF_CELLS):
                # print (f"x:{x} y:{y}")
                # for testing make the is_travelable random
                is_travelable = False
                travelled = -1
                traced = False
                a_row.append(cell.Cell(self.DEFAULT_WEIGHT, x, y, is_travelable, travelled, traced))
                x += 1
            y += 1
            self.board.append(a_row)
        self.my_maze = maze.Maze(self.board)
        self.rat = mouse.Mouse(0,config.max_y_coord(),0,0,0,self)

    def update_circle(self,id,x,y):
        oldcircle = None
        if id:
            oldcircle = self.canvas.find_withtag(id)
            self.canvas.delete(oldcircle)
        oldcircle =  self.canvas.create_oval(x,y,x+config.MOUSE_RADIUS,
                                             y+config.MOUSE_RADIUS,
                                             fill=config.MOUSE_FILL_COLOR)
        self.root.update()
        return oldcircle

    def draw_circle_suggested(self,id,delete,x,y):
        oldcircle = None
        if delete:
            oldcircle = self.canvas.find_withtag(id)
            self.canvas.delete(oldcircle)
        else:
            oldcircle =  self.canvas.create_oval(x,y,x+config.MOUSE_RADIUS,
                                                 y+config.MOUSE_RADIUS,
                                                 fill=config.SUGGESTED_MOUSE_FILL_COLOR)
            self.root.update()
        return oldcircle

    def draw_line(self,x1,y1,x2,y2):
        last_line = self.canvas.create_line(x1,y1,x2,y2,fill=config.PATH_LINE_COLOR, width=2)
        self.canvas.itemconfigure(last_line, tags="path")
        self.root.update()

    def move_mouse(self,rat):
        for k in range(config.num_learning_steps):#rat.get_v() > rat.MIN:
            self.update_status(f"{k}")
            bool = False
            coords = [0,config.max_y_coord()]
            while bool is False:
                coords = rat.get_next_coordinate(rat.get_x(), rat.get_y(),
                                             rat.get_t())

                x_f = coords[0]
                y_f = coords[1]
                # draw suggested debug
                # debug
                #old_suggested_circle = self.draw_circle_suggested(None,False,x_f,y_f)
                for  i in range (config.NUMBER_OF_CELLS):
                    break_loop = False
                    for j in range (config.NUMBER_OF_CELLS):
                        if self.board[i][j].is_travellable:
                            if rat.intersect(rat.get_x(),rat.get_y(),
                                             x_f,
                                             y_f,
                                             config.CELL_WIDTH*j,
                                             config.CELL_WIDTH*i):
                                bool = False
                                break_loop = True
                                break
                            else:
                                bool = True
                    if break_loop:
                        break
            # exit_cell_x1 = 580 exit_cell_x1 = 600 exit_cell_y1 = 0 exit_cell_y2 = 20
            if x_f > config.exit_cell_x1() \
                    and x_f < config.exit_cell_x2() \
                    and y_f > config.exit_cell_y1() \
                    and y_f < config.exit_cell_y2():
                rat.move(x_f,y_f)
                self.board[int(y_f // config.CELL_WIDTH)][int(x_f //config.CELL_WIDTH)].travelled = rat.get_t()
                self.my_maze.update_weight(rat)
                break
            row = int(y_f // config.CELL_WIDTH)
            col = int(x_f // config.CELL_WIDTH)

            if rat.get_t()%10 == 0:
                self.my_maze.update_weight(rat)
            if not self.board[int(y_f // config.CELL_WIDTH)][int(x_f // config.CELL_WIDTH)].is_travellable:
                rat.move(x_f,y_f)
                self.board[int(y_f // config.CELL_WIDTH)][int(x_f // config.CELL_WIDTH)].travelled = rat.get_t()
                rat.set_t(rat.get_t()+1)
        # update for last time
        self.my_maze.update_weight(rat)

    def path(self,rat):
        x_f = rat.get_x()
        y_f = rat.get_y()
        rat.set_x(0)
        rat.set_y(config.max_y_coord()-1)
        limit_x = (x_f//config.CELL_WIDTH)*config.CELL_WIDTH
        limit_y = (y_f//config.CELL_WIDTH)*config.CELL_WIDTH

        bool_1 = rat.get_x() > limit_x and rat.get_x() < limit_x+config.CELL_WIDTH
        bool_2 = rat.get_y() > limit_y and rat.get_y() < limit_y+config.CELL_WIDTH
        bool_3 = bool_1 and bool_2

        while not int(self.board[rat.get_y()//config.CELL_WIDTH][rat.get_x()//config.CELL_WIDTH].get_weight()) == 2:
            max = -1
            i_max = 0
            j_max = 0
            for i in [-1,0,1]: #range(-1,2):
                for j in [-1,0,1]: #range (-1,2):
                    col = rat.get_x()//config.CELL_WIDTH
                    row = rat.get_y()//config.CELL_WIDTH
                    if not i == 0 or not j == 0:
                        if (row+i) >= 0 and (row+i) <=config.NUMBER_OF_CELLS-1 and (col+j) >= 0 and (col+j) <=config.NUMBER_OF_CELLS-1:
                            if not self.board[row+i][col+j].traced:
                                if self.board[row+i][col+j].get_weight() > max:
                                    max = self.board[row+i][col+j].get_weight()
                                    i_max = i
                                    j_max = j

            if max == -1:
                print("Could not select a cell to move")
                for i in [-1, 0, 1]:
                    for j in [-1, 0, 1]:
                        if not i == 0 or not j == 0:
                            if (row + i) >= 0 and (row + i) <= config.NUMBER_OF_CELLS - 1 and (col + j) >= 0 and (col + j) <= config.NUMBER_OF_CELLS - 1:
                                    if self.board[row + i][col + j].get_weight() > max:
                                        max = self.board[row + i][col + j].get_weight()
                                        i_max = i
                                        j_max = j

            print("Then picked max ",max)
            rat.move(rat.get_x()+config.CELL_WIDTH*j_max, rat.get_y()+config.CELL_WIDTH*i_max)
            self.board[row][col].traced = True

    def print_board(self):
        # print header
        print("{:8} ".format(''),end='')
        for i in range(config.NUMBER_OF_CELLS):
            print("{:8.0f} ".format(i),end='')
        print()
        for i in range(config.NUMBER_OF_CELLS):
            print("{:8.0f} ".format(i), end='')
            for j in range(config.NUMBER_OF_CELLS):
                print(self.board[i][j],end='')
            print()


def main():
    memmap = MemoryModel()
    memmap.init_board()
    memmap.draw_board()

if __name__ == '__main__':
    main()
