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

class MemoryModel (object):
    CELL_WIDTH = 20 # square width
    DEFAULT_WEIGHT =0.1  # default weight
    WALKABLE_CELL_COLOR = "white"
    BLOCKED_CELL_COLOR = "gray"
    NUM_DIRECTIONS = 200


    def __init__(self):
        self.selection_strategy_max = True
        self.rundata = 1
        self.marking_reward_space = False
        self.reward_start = None
        self.reward_end = None

    def draw_board(self):
        self.root = tkinter.Tk()  # start the gui engine
        self.strategy_var = IntVar()
        self.strategy_var.set(1)
        ## TOP CONTROL BUTTON FRAME
        self.top_frame = tkinter.Frame(self.root)
        self.top_frame.grid(row=0, column=0)
        ## CONTROLS ROW 1
        self.learning_button = tkinter.Button(self.top_frame, text='START LEARNING',
                                        width=20,
                                        command=self.start_learning)

        self.path_button = tkinter.Button(self.top_frame, text='FIND PATH',
                                              width=20,
                                              command=self.find_path_handler)

        self.collect_data_button = tkinter.Button(self.top_frame, text='COLLECT DATA',
                                          width=20,
                                          command=self.collect_data)
        self.special_path_button = tkinter.Button(self.top_frame, text='SPECIAL PATH',
                                                  width=20,
                                                  command=self.find_special_path_handler)
        self.mark_goal_button = tkinter.Button(self.top_frame, text='SELECT REWARD SPACE',
                                                  width=20,
                                                  command=self.start_marking_reward_handler)

        #self.load_maze_button = tkinter.Button(self.top_frame, text='LOAD MAZE',
        #                                      width=20,
        #                           command=self.load_maze)
        ## CONTROL ROW 2
        self.iterations = tkinter.Entry (self.top_frame)
        self.iterations.insert(0,str(config.num_learning_steps))
        #self.apply_button = tkinter.Button(self.top_frame, text='APPLY',
        #                                  width=20,
        #                                  command=self.apply_config)
        label = tkinter.Label(self.top_frame, text='ITERATIONS',
                                           width=20)

        self.strategy = tkinter.Checkbutton(self.top_frame,text="Max weight strategy", var = self.strategy_var)

        self.learning_button.grid(row=0, column=0)
        self.path_button.grid(row=0, column=1)
        self.collect_data_button.grid(row = 0, column = 2)
        self.special_path_button.grid(row=0, column=3)
        self.mark_goal_button.grid(row=0, column=4)
        #self.load_maze_button.grid(row=0, column=2)
        label.grid(row=1, column=0)
        self.iterations.grid(row=1, column=1)
        #self.apply_button.grid(row=1, column=2)
        self.strategy.grid(row=1,column=3)

        ## BOARD CANVASE FRAME
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
        self.canvas.bind("<Button-1>", self.on_clicked)
        ## BOTTOM STATUS FRAME
        self.status = tkinter.Label(self.root, text="STATUS:")
        self.status.grid(row=2, column=0)

        # now create rectangle
        for i in range(config.NUMBER_OF_CELLS):
            for j in range(config.NUMBER_OF_CELLS):
                cell = self.board[i][j]
                # rectangle need (x1,y1) and x2,y2)
                if cell.is_travellable:
                    fill_color = self.BLOCKED_CELL_COLOR
                else:
                    fill_color = self.WALKABLE_CELL_COLOR
                box = self.canvas.create_rectangle(self.CELL_WIDTH * j,
                                              self.CELL_WIDTH * i,
                                              self.CELL_WIDTH * (j + 1),
                                              self.CELL_WIDTH * (i + 1),
                                              fill=fill_color,tag=self.to_tag(i,j))
        # you need to call this so that the GUI start running

        self.root.mainloop()
    def update_status(self,txt):
        self.status.configure(text=txt)
    def start_marking_reward_handler(self):
        self.marking_reward_space = True
        self.reward_start = None
        self.reward_end = None

    def apply_config(self):
        if self.iterations.get():
            config.num_learning_steps=int(self.iterations.get())

    def to_tag(self,row,col):
        return f"{row}-{col}"

    def from_tag(self,tag):
        parts = tag.split("-")
        return int(parts[0]), int(parts[1])

    def on_clicked(self,e):
        if not self.marking_reward_space: # not in marking mode
            return
        found_rectangle = False
        shape =-1
        shape_x = e.x
        shape_y = e.y
        while not found_rectangle:
            shape = self.canvas.find_closest(shape_x, shape_y)
            shape_tag = self.canvas.gettags(shape)[0]
            if shape_tag != "path":
                found_rectangle = True
            else:
                shape_x +=2
                shape_y +=2

        row, col = self.from_tag(self.canvas.gettags(shape)[0])
        fill_color=""
        if not self.reward_start:  # we are selecting start
            fill_color = "red"
            self.reward_start = [e.x,e.y]
        elif not self.reward_end:
            fill_color = "green"
            self.reward_end = [row,col]
            self.marking_reward_space = False

        self.canvas.itemconfig(shape, fill=fill_color)

    def start_learning(self):
        self.rundata = rundata.RunData()
        self.apply_config()
        self.canvas.delete("path")
        self.move_mouse(self.rat)
        self.print_board()

    def collect_data(self):
        f = open("data.csv", "w+")
        for i in range(100):
            if i==0:
                f.write(rundata.RunData.report_heading()+"\n")
            self.update_status(f"LEARNING - RUN #:{i}")
            self.start_learning()
            success = True
            for n in [5,10,15,20,30,40,60,80,100,150,200,300,400,600,1000]:
                self.update_status(f"FIND PATH - RUN #:{i} NUM_DIRECTIONS #:{n}")
                success = self.find_path(n)
                if not success:
                    break
                f.write(str(self.rundata) + "\n")
        f.close()

    def find_special_path(self,num_directions):
        self.selection_strategy_max = bool(self.strategy_var.get())
        self.apply_config()
        self.canvas.delete("path")
        self.canvas.update()
        ret = self.path(self.rat, num_directions,True)
        self.print_board()
        return ret

    def find_path_handler(self):
        self.find_path(self.NUM_DIRECTIONS)

    def find_special_path_handler(self):
        self.find_special_path(self.NUM_DIRECTIONS)

    def find_path(self,num_directions):
        self.selection_strategy_max = bool(self.strategy_var.get())
        self.apply_config()
        self.canvas.delete("path")
        self.canvas.update()
        ret = self.path(self.rat,num_directions,False)
        self.print_board()
        return ret

    def load_maze(self):
        print('loading maze')
        file_path = filedialog.askopenfilename()
        self.my_maze.load(file_path)

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
                first_travelled = -1
                traced = False
                a_row.append(cell.Cell(self.DEFAULT_WEIGHT, x, y, is_travelable, travelled, first_travelled, traced))
                x += 1
            y += 1
            self.board.append(a_row)
        self.my_maze = maze.Maze(self.board)
        self.my_maze.setup_default_maze()

        self.rat = mouse.Mouse(0,599,0,0,0,self)

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

    def reset_velocity(self,rat):
        rat.set_v_x(0)
        rat.set_v_y(0)

    def move_mouse(self,rat):
        self.reset_mouse(rat)
        displacements = []
        time = 0
        for q in range (config.num_learning_steps):
        #while not self.isOnLastCell(rat.get_x(),rat.get_y()):
            coords = [0,config.max_y_coord()]
            coords = rat.get_next_coor(rat.get_x(), rat.get_y())
            x_f = coords[0]
            y_f = coords[1]
            if x_f<0 or x_f >=600 or y_f<0 or y_f >=600:
                continue
            row = rat.get_y() // config.CELL_WIDTH
            col = rat.get_x()//config.CELL_WIDTH

            for  i in range (-1,2,1):
                for j in range (-1,2,1):
                    if row+i >=0 and row+i <=config.NUMBER_OF_CELLS-1 and col+j>=0 and col+j <=config.NUMBER_OF_CELLS-1:
                        if self.board[int(row+i)][int(col+j)].is_travellable:
                            # ORIGINAL arr = rat.intersect2(rat.get_x(),rat.get_y(),x_f,y_f,config.CELL_WIDTH*j,config.CELL_WIDTH*i)
                            int_arr = rat.intersect2(rat.get_x(), rat.get_y(), x_f, y_f, config.CELL_WIDTH * (col+j), config.CELL_WIDTH *(row+ i))
                            if int_arr[0]:
                                arr = int_arr[1] # array of array of intersection points
                                if len(arr) == 1:
                                    x_f = arr[0][0]
                                    y_f = arr[0][1]
                                if len(arr) == 2:
                                    distance1 = math.sqrt(math.pow(rat.get_x()-arr[0][0],2)+math.pow(rat.get_y()-arr[0][1],2))
                                    distance2 = math.sqrt(math.pow(rat.get_x()-arr[1][0],2)+math.pow(rat.get_y()-arr[1][1],2))
                                    if distance1 > distance2:
                                        x_f = arr[1][0]
                                        y_f = arr[1][1]
                                    else:
                                        x_f = arr[0][0]
                                        y_f = arr[0][1]

                                self.reset_velocity(rat)
                    vals = rat.off_grid(x_f, y_f)  # of the grid
                    if vals[0]:
                        p1 = Point2D(rat.get_x(), rat.get_y())
                        p2 = Point2D(x_f, y_f)
                        line = Segment2D(p1, p2)
                        if vals[1] == 0:
                            int_point = config.line_intersection(line,Line2D((0,0),(0,2)))
                            if int_point and len(int_point):
                                x_f = float(int_point[0].x)
                                y_f = float(int_point[0].y)
                            self.reset_velocity(rat)
                        elif vals[1] == 1:
                            int_point = config.line_intersection(line, Line2D((600, 0), (600, 2)))
                            if int_point and len(int_point):
                                x_f = float(int_point[0].x)
                                y_f = float(int_point[0].y)
                            self.reset_velocity(rat)
                        elif vals[1] == 2:
                            int_point = config.line_intersection(line, Line2D((0, 0), (2, 0)))
                            if int_point and len(int_point):
                                x_f = float(int_point[0].x)
                                y_f = float(int_point[0].y)
                            self.reset_velocity(rat)
                        elif vals[1] == 3:
                            int_point = config.line_intersection(line, Line2D((0, 600), (2, 600)))
                            if int_point and len(int_point):
                                x_f = float(int_point[0].x)
                                y_f = float(int_point[0].y)
                            self.reset_velocity(rat)
            #if self.isOnLastCell(x_f,y_f):
                #rat.move(x_f,y_f)
                #self.board[int((y_f-0.00001) // config.CELL_WIDTH)][int((x_f-0.00001) //config.CELL_WIDTH)].travelled = rat.get_t()
                #self.my_maze.update_weight(rat)
                #break
            row = int(y_f // config.CELL_WIDTH)
            col = int(x_f // config.CELL_WIDTH)

            if rat.get_t()%10 == 0:
                self.my_maze.update_weight(rat)
                zero_distance = sqrt(math.pow(rat.get_x()-0,2)+math.pow(rat.get_y()-599,2))
                displacements.append(zero_distance)

            row = int((y_f)// config.CELL_WIDTH)
            col = int((x_f) // config.CELL_WIDTH)
            if not self.board[row][col].is_travellable:
                self.my_maze.update_weight(rat)
                rat.move(x_f,y_f)
                self.board[row][col].travelled = rat.get_t()
                if self.board[row][col].first_travelled == -1:
                    self.board[row][col].first_travelled = rat.get_t()
                    for a in range (30):
                        for b in range (30):
                            self.board[row][col].storage[a][b] = self.board[a][b].get_weight()

                rat.set_t(rat.get_t()+1)
                time = time + 1
            else:
                config.p('*')
        # update for last time
        self.my_maze.update_weight(rat)
        count = 0
        for row in range (30):
            for col in range(30):
                if self.board[row][col].weight>0:
                    count = count + 1
        self.rundata.num_squares = count
        self.rundata.learning_length = rat.get_distance()
        self.rundata.displacements = displacements
        self.rundata.time = time
        self.update_status(f"Learning Length: {rat.get_distance()}")

    def isOnLastCell(self,x_f,y_f):
        # check to see the points are on last cell
        return  x_f > config.exit_cell_x1() and x_f < config.exit_cell_x2() and y_f > config.exit_cell_y1() and y_f < config.exit_cell_y2()

    def path(self,rat,num_directions,special):
        if special:
            reward_row = 10
            reward_col = 10
            if self.reward_end:
               reward_row = self.reward_end[0]
               reward_col = self.reward_end[1]
            self.my_maze.reassign_weight(rat,reward_row,reward_col)
        learning_distance = rat.get_distance()
        rat.set_distance(0)
        starting_x = 0
        starting_y = 599
        if special and not self.reward_start:
            starting_x = self.reward_start[0]
            starting_y = self.reward_start[1]

        rat.set_x(starting_x)
        rat.set_y(starting_y)
        rat.set_v_x(0)
        rat.set_v_y(0)
        x_f = rat.get_x()
        y_f = rat.get_y()
        limit_x = (x_f//config.CELL_WIDTH)*config.CELL_WIDTH
        limit_y = (y_f//config.CELL_WIDTH)*config.CELL_WIDTH
        arr = []
        weights = []
        weights_map = {}
        trap_count =  0
        cont_count = 0
        counter = 0

        while not int(self.board[int(rat.get_y()//config.CELL_WIDTH)][int(rat.get_x()//config.CELL_WIDTH)].get_weight()) == 2:
            weights.clear()
            arr.clear()
            for i in range (num_directions):
                arr.append(float(np.random.random()*360))
            for j in range (num_directions):
                v_x = copy.copy(rat.get_v_x())
                v_y = copy.copy(rat.get_v_y())
                next_coords = rat.get_next_coor_directed(rat.get_x(), rat.get_y(), arr[j])
                x_temp = next_coords[0]
                y_temp = next_coords[1]
                row = int(y_temp//config.CELL_WIDTH)
                col = int(x_temp//config.CELL_WIDTH)
                if row >= 0 and row <=29 and col >=0 and col<=29:
                    w = self.board[row][col].get_weight()
                    tr = y_f//config.CELL_WIDTH
                    tc = x_f//config.CELL_WIDTH
                    w1 = self.board[int(y_f//config.CELL_WIDTH)][int(x_f//config.CELL_WIDTH)].get_weight()
                    if not self.board[row][col].is_travellable and self.board[row][col].get_weight() >= self.board[int(y_f//config.CELL_WIDTH)][int(x_f//config.CELL_WIDTH)].get_weight():
                        if self.selection_strategy_max:
                            weights.append([self.board[row][col].get_weight(), x_temp,y_temp])
                            weights_map[self.board[row][col].get_weight()] = [x_temp,y_temp]
                        else:
                            rat.move(x_temp,y_temp)
                            break
                    else:
                        rat.set_v_x(v_x)
                        rat.set_v_y(v_y)
                else:
                    rat.set_v_x(v_x)
                    rat.set_v_y(v_y)

            if self.selection_strategy_max and weights_map:

                if cont_count >= 100:
                    weights_map.pop(max(weights_map))
                    if weights_map:
                        b_max = weights_map[max(weights_map)]
                    else:
                        return False
                else:
                    b_max = weights_map[max(weights_map)]
                new_row = b_max[1] // 20
                new_col = b_max[0] // 20
                prev_row = rat.get_y() // 20
                prev_col = rat.get_x() // 20
                if new_row == prev_row and new_col == prev_col:
                    cont_count +=1
                    print("TRAPPED IN THE SAME CELL ",new_row,new_col)
                else:
                    cont_count =0
                if cont_count >= 10:
                    trap_count +=1
                    print("TRAP COUNT INCR ",trap_count)
                if trap_count > 2000:
                    return False
                rat.move(b_max[0], b_max[1])


        # update rundata
        self.rundata.num_directions =len(arr)
        self.rundata.num_traps = trap_count
        self.rundata.search_length = rat.get_distance()
        return True

    def reset_mouse(self, rat):
        rat.set_x(0)
        rat.set_y(599)
        rat.set_v_x(0)
        rat.set_v_y(0)
        for row in range(30):
            for col in range(30):
                self.board[row][col].set_weight(-1)
                self.board[row][col].travelled = -1
                self.board[row][col].traced = False

    def print_board(self):
        # print header
        config.p("{:8} ".format(''))
        for i in range(config.NUMBER_OF_CELLS):
            config.p("{:8.0f} ".format(i))
        config.pl()
        for i in range(config.NUMBER_OF_CELLS):
            config.p("{:8.0f} ".format(i))
            for j in range(config.NUMBER_OF_CELLS):
                config.p(self.board[i][j])
            config.pl()


def main():

    memmap = MemoryModel()
    memmap.init_board()
    memmap.draw_board()




if __name__ == '__main__':
    main()
