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
from tkinter import StringVar
from datetime import datetime

class MemoryModel (object):

    CELL_WIDTH = 20 # square width
    DEFAULT_WEIGHT =0.1  # default weight
    WALKABLE_CELL_COLOR = "white"
    BLOCKED_CELL_COLOR = "gray"
    NUM_DIRECTIONS = 1000


    def __init__(self):
        self.selection_strategy_max = True #max selection startgy deprecate it
        self.rundata = 1
        self.marking_reward_space = False
        self.reward_start = None
        self.reward_end = None

    def draw_board(self):
        self.root = tkinter.Tk()  # start the gui engine
        self.strategy_var = IntVar()
        self.avoid_gray  = IntVar()
        self.damage_interval_var = StringVar()
        self.damage_var = IntVar()
        self.spread_damage_var = IntVar()
        self.damage_count_var = StringVar()

        self.avoid_gray.set(1)
        self.strategy_var.set(1)
        self.damage_var.set(1)
        self.damage_interval_var.set("1")
        self.damage_count_var.set("1")

        ## TOP CONTROL BUTTON FRAME
        self.top_frame = tkinter.Frame(self.root)
        self.top_frame.grid(row=0, column=0)
        self.buttons_frame = tkinter.Frame(self.top_frame)
        self.config_frame = tkinter.Frame(self.top_frame)
        self.buttons_frame.grid(row=0,column=0)
        self.config_frame.grid(row=1, column=0)

        ## CONTROLS ROW 1
        button_panel_label = tkinter.Label(self.buttons_frame, text='---CONTROLS---')
        self.learning_button = tkinter.Button(self.buttons_frame, text='START LEARNING',
                                        width=20,
                                        command=self.start_learning)

        self.path_button = tkinter.Button(self.buttons_frame, text='FIND PATH',
                                              width=20,
                                              command=self.find_path_handler_regular)

        self.collect_data_button = tkinter.Button(self.buttons_frame, text='COLLECT DATA',
                                          width=20,
                                          command=self.collect_data)
        self.special_path_button = tkinter.Button(self.buttons_frame, text='SPECIAL PATH',
                                                  width=20,
                                                  command=self.find_special_path_handler)
        self.mark_goal_button = tkinter.Button(self.buttons_frame, text='SELECT REWARD SPACE',
                                                  width=20,
                                                  command=self.start_marking_reward_handler)
        self.omnicient_button = tkinter.Button(self.buttons_frame, text='OMNICIENT SUCCESSOR',
                                                  width=20,
                                                  command=self.find_path_handler)


        ## CONTROL ROW 2
        config_panel_label = tkinter.Label(self.config_frame, text='--- CONFIG PARAMS ----')
        self.iterations = tkinter.Entry (self.config_frame,width=10)
        damage_interval_label = tkinter.Label(self.config_frame, text='DAMAGE INTERVAL',
                              width=20)
        self.damage_interval_entry = tkinter.Entry (self.config_frame,width=5,textvariable = self.damage_interval_var)

        damage_count_label = tkinter.Label(self.config_frame, text='DAMAGE COUNT',
                                              width=20)
        self.damage_count_entry = tkinter.Entry(self.config_frame, width=5, textvariable=self.damage_count_var)

        self.iterations.insert(0,str(config.num_learning_steps))
        label = tkinter.Label(self.config_frame, text='ITERATIONS',
                                           width=10)

        self.strategy = tkinter.Checkbutton(self.config_frame,text="Max weight strategy", var = self.strategy_var)
        self.avoid_gray_chk = tkinter.Checkbutton(self.config_frame, text="Avoid gray", var=self.avoid_gray)
        self.damage_chk = tkinter.Checkbutton(self.config_frame, text="Damage", var=self.damage_var)
        self.spread_damage_chk = tkinter.Checkbutton(self.config_frame, text="Spread Damage", var=self.spread_damage_var)

        button_panel_label.grid(row=0,column=0)
        self.learning_button.grid(row=1, column=0)
        self.path_button.grid(row=2, column=0)
        self.special_path_button.grid(row=3, column=0)
        self.omnicient_button.grid(row=4, column=0)

        self.collect_data_button.grid(row = 5, column = 0)
        self.mark_goal_button.grid(row=6, column=0)

        tkinter.Label(self.config_frame).grid(row=0,column=0)
        config_panel_label.grid(row=2,column=0,columnspan=2)
        label.grid(row=4, column=0)
        self.iterations.grid(row=4, column=1)
        self.strategy.grid(sticky="W",row=5,column=1)
        self.avoid_gray_chk.grid(sticky="W",row=6,column=1)
        self.damage_chk.grid(sticky="W", row=7, column=1)
        self.spread_damage_chk.grid(sticky="W", row=8, column=1)
        damage_interval_label.grid(row=9,column=0)
        self.damage_interval_entry.grid(sticky="W", row=9, column=1)
        damage_count_label.grid(row=10, column=0)
        self.damage_count_entry.grid(sticky="W", row=10, column=1)

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
        canvas_frame.grid(row=0,column=1)
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
                                              fill=fill_color)
        # you need to call this so that the GUI start running

        self.root.mainloop()

    def update_status(self,txt):
        """
        Update status bar
        :param txt:
        :return:
        """
        self.status.configure(text=txt)

    def start_marking_reward_handler(self):
        """
        To keep track of the marking ow reward staart and end
        :return:
        """
        self.marking_reward_space = True
        self.reward_start = None
        self.reward_end = None

    def apply_config(self):
        """
        Update whatever configurations
        :return:
        """
        if self.iterations.get():
            config.num_learning_steps=int(self.iterations.get())

    def on_clicked(self,e):
        if not self.marking_reward_space: # not in marking mode
            return
        row = e.y//20
        col = e.x //20
        fill_color=""
        if not self.reward_start:  # we are selecting start
            fill_color = "red2"
            self.reward_start = [e.x,e.y]
        elif not self.reward_end:
            fill_color = "purple"
            self.reward_end = [e.x,e.y]
            self.marking_reward_space = False

        self.canvas.create_oval(e.x, e.y, e.x + config.MOUSE_RADIUS,
                                            e.y + config.MOUSE_RADIUS,
                                            fill=fill_color)

    def start_learning(self):
        self.rundata = rundata.RunData()
        self.apply_config()
        self.canvas.delete("path") # remove all paths
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
        ret = self.path(self.rat, num_directions,True,False)
        return ret

    def find_path_handler(self):
        self.find_path(self.NUM_DIRECTIONS)

    def find_path_handler_regular(self):
        self.find_path_regular(self.NUM_DIRECTIONS)

    def find_special_path_handler(self):
        self.find_special_path(self.NUM_DIRECTIONS)

    def find_path(self,num_directions):
        self.selection_strategy_max = bool(self.strategy_var.get())
        self.apply_config()
        self.canvas.delete("path")
        self.canvas.update()
        ret = self.path(self.rat,num_directions,True,True)
        return ret

    def find_path_regular(self,num_directions):
        self.selection_strategy_max = bool(self.strategy_var.get())
        self.apply_config()
        self.canvas.delete("path")
        self.canvas.update()
        ret = self.path(self.rat,num_directions,False,False)
        return ret

    def load_maze(self):
        file_path = filedialog.askopenfilename()
        self.my_maze.load(file_path)

    def init_board(self):
        x = 0
        y = 0
        self.board = []
        #
        # initialize the board with cells
        #

        for row in range(config.NUMBER_OF_CELLS):
            x = 0
            a_row = []
            for col in range(config.NUMBER_OF_CELLS):
                # print (f"x:{x} y:{y}")
                # for testing make the is_travelable random
                is_travellable = False
                travelled = -1
                first_travelled = -1
                traced = False
                a_row.append(cell.Cell(self.DEFAULT_WEIGHT, x, y, is_travellable, travelled, first_travelled, traced))
                x += 1
            y += 1
            self.board.append(a_row)
        #
        # Initialize the data metrix
        #
        b_row = []
        self.matrix = np.identity(900)
        print(self.matrix)
        w = []
        T = []
        for d in range (900):
            w.append(0)
            T.append([0]*900)
        self.my_maze = maze.Maze(self,self.board, self.matrix, w,T)
        self.my_maze.setup_default_maze()

        self.rat = mouse.Mouse(0,599,0,0,0,self)

    def make_cell_damaged(self,row,col):
        x = col*config.CELL_WIDTH+2
        y = row*config.CELL_WIDTH+2
        c = self.canvas.find_closest(x,y)
        self.canvas.itemconfig(c, fill="black")
        self.canvas.update()

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

    def get_closest_collision_point(self,rat,x, y, new_x, new_y, row, col):
        # Find the closes collision point
        # Parameters
        #   rat - Mouse
        #   x - Current x position
        #   y - Current y position
        #   new_x - new x position we are trying to test
        #   new_y - new y position we are trying to test
        #   row,col - row,col of the cell we are trying to check againt typically gray cells
        #
        # Returns:
        #   If have intersection [True,closest x, colsest y]
        #   If no intersection [False]
        lower_x = config.CELL_WIDTH * col
        lower_y = config.CELL_WIDTH * row

        int_arr = mouse.Mouse.intersect2(x, y, new_x, new_y, lower_x,lower_y)
        if int_arr[0]:  # yes there is an intersection
            arr = int_arr[1]  # array of array of intersection points
            if len(arr) == 1:
                return [True,arr[0][0],arr[0][1]]
            elif len(arr) == 2:
                distance1 = math.sqrt(math.pow(rat.get_x() - arr[0][0], 2) + math.pow(rat.get_y() - arr[0][1], 2))
                distance2 = math.sqrt(math.pow(rat.get_x() - arr[1][0], 2) + math.pow(rat.get_y() - arr[1][1], 2))
                if distance1 > distance2:
                    return [True, arr[1][0],arr[1][1]]
                else:
                    return [True,arr[0][0],arr[0][1]]
        return [False]

    def is_in_range(self,line, x, y):
        x1 = line[0][0]
        y1 = line[0][1]
        x2 = line[1][0]
        y2 = line[1][1]
        if x1 != x and x2 != x:
            if min(x1, x2, x) == x or max(x1, x2, x) == x:
                return False
        if y1 != y and y2 != y:
            if min(y1, y2, y) == y or max(y1, y2, y) == y:
                return False
        return True

    def point_given_distance(self,x1, y1, x2, y2, l):
        # find slope
        infinite_slope = x2 == x1
        m = 0
        a_x = a_y = b_x = b_y = 0
        if not infinite_slope:
            m = (y2 - y1) / (x2 - x1)
        if infinite_slope:
            a_x = x1
            a_y = y1 + l
            b_x = x1
            b_y = y1 - l
        elif m == 0:
            a_x = x1 + l
            a_y = y1
            b_x = x1 - l
            b_y = y1
        else:
            dx = (l / math.sqrt(1 + (m * m)))
            dy = m * dx
            a_x = x1 + dx
            a_y = y1 + dy
            b_x = x1 - dx
            b_y = y1 - dy
        # not make sure points are with in the segment
        line = [[x1, y1], [x2, y2]]
        if self.is_in_range(line, a_x, a_y):
            return [a_x, a_y]
        if self.is_in_range(line, b_x, b_y):
            [b_x, b_y]
        return []


    def is_intersect_wth_gray_cells_new(self,x1,y1,new_x, new_y):
        #if not bool(self.avoid_gray.get()):
        #    return False
        start_row = int(min(y1,new_y)//config.CELL_WIDTH)
        start_col = int(min(x1, new_x) // config.CELL_WIDTH)
        end_row = int(max(y1, new_y) // config.CELL_WIDTH)
        end_col = int(max(x1, new_x) // config.CELL_WIDTH)
        for row in range(start_row,end_row+1):
            for col in range(start_col, end_col + 1):
                if self.board[row][col].is_travellable:
                    lower_x = config.CELL_WIDTH * col
                    lower_y = config.CELL_WIDTH * row
                    arr = mouse.Mouse.intersect2(x1, y1, new_x, new_y, lower_x, lower_y)
                    if arr[0]:
                        config.dl(f"AVOIDING ({new_x},{new_y})")
                        return True
        return False

    def is_intersect_wth_gray_cells(self, rat, new_x, new_y):
        return self.is_intersect_wth_gray_cells_x(rat.get_x(),rat.get_y(),new_x, new_y,bool(self.avoid_gray.get()),self.board)

    def is_intersect_wth_gray_cells_x(self,x1,y1, new_x, new_y,avoid_gray_flag,board):
        if not avoid_gray_flag:
            return False
        length = math.sqrt(math.pow(x1 - new_x, 2) + math.pow(y1 - new_y, 2))

        d=0
        delta=1

        prev_row = -1
        prev_col = -1
        my_paths = ""
        while d<=math.ceil(length):
            point_in_line = self.point_given_distance(x1,y1,new_x,new_y,d)
            if point_in_line:
                row = int(point_in_line[1]//config.CELL_WIDTH)
                col = int(point_in_line[0]//config.CELL_WIDTH)
                if prev_row != row or prev_col != col:
                    prev_row = row
                    prev_col = col
                    my_paths = f"{my_paths}, ({row},{col}) "
                    print(f"CELL {row},{col}")
                    if board[row][col].is_travellable:  # gray cell
                        #print(f"AVOIDING {row},{col}")
                        return True
                        #lower_x = config.CELL_WIDTH * col
                        #lower_y = config.CELL_WIDTH * row
                        #arr = rat.intersect2(rat.get_x(), rat.get_y(), new_x, new_y, lower_x, lower_y)
                        #if arr[0]:
                            #print(f"AVOIDING JUMP ({row},{col})")
                        #    return True
            d +=delta
        s_row = y1//config.CELL_WIDTH
        s_col = x1//config.CELL_WIDTH
        e_row = new_y // config.CELL_WIDTH
        e_col = new_x // config.CELL_WIDTH
        print(f"({s_row},{s_col}) - ({e_row},{e_col}) LENGTH {length} paths {my_paths}")
        return False

    def move_mouse(self,rat):
        self.reset_mouse(rat)

        self.reward_start = [rat.get_x(),rat.get_y()]

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
                                elif len(arr) == 2:
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
                #self.my_maze.update_weight(rat)
                self.my_maze.update_matrix(x_f,y_f,rat)

                #first_index = int(rat.get_y()//20*30+rat.get_x()//20)
                #second_index = int(y_f//20*30+x_f//20)
                #for c in range (900):
                #    if c == first_index:
                #        self.my_maze.matrix[first_index][c] = self.my_maze.matrix[first_index][c]+rat.ALPHA*(1+rat.GAMMA*self.my_maze.matrix[second_index][c]-self.my_maze.matrix[first_index][c])
                #    else:
                #        self.my_maze.matrix[first_index][c] = self.my_maze.matrix[first_index][c] + rat.ALPHA*(0 + rat.GAMMA * self.my_maze.matrix[second_index][c] - self.my_maze.matrix[first_index][c])
                rat.move(x_f,y_f)
                self.board[row][col].travelled = rat.get_t()
                self.my_maze.update_weight(rat)
                self.board[row][col].first_travelled = rat.get_t()
                for a in range (30):
                    for b in range (30):
                        self.board[row][col].storage[a][b] = self.board[a][b].get_weight()

                rat.set_t(rat.get_t()+1)
                time = time + 1
            else:
                config.i('*')
            self.update_status(f"Learning:{q}")
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
        self.reward_end = [rat.get_x(), rat.get_y()]

    def isOnLastCell(self,x_f,y_f):
        # check to see the points are on last cell
        return  x_f > config.exit_cell_x1() and x_f < config.exit_cell_x2() and y_f > config.exit_cell_y1() and y_f < config.exit_cell_y2()

    def path(self,rat,num_directions,special,omnicient):

        if bool(self.damage_var.get()):  # if damage selected
            interval_val = int(self.damage_interval_var.get())
            count_val = int(self.damage_count_var.get())
            self.my_maze.setup_damage(interval=interval_val,count=count_val,spread=bool(self.spread_damage_var.get())) # setup the damaging

        if special:
            config.il(f" start({self.reward_start[0]},{self.reward_start[1]}) end ({self.reward_end[0]},{self.reward_end[1]})")
            reward_row = 10
            reward_col = 10
            if self.reward_end:
                reward_x = self.reward_end[0]
                reward_y = self.reward_end[1]
                reward_row = reward_y // 20
                reward_col = reward_x // 20
            if omnicient:
                self.my_maze.create_T(rat)
                self.my_maze.create_weights_omnicient(rat,reward_row,reward_col)
        else:
            reward_x = rat.get_x()
            reward_y = rat.get_y()
        learning_distance = rat.get_distance()
        rat.set_distance(0)
        starting_x = 0
        starting_y = 599
        if special and self.reward_start:
            starting_x = self.reward_start[0]
            starting_y = self.reward_start[1]
            start_row = starting_y // 20
            start_col = starting_x // 20

            if 2==1 and self.board[start_row][start_col].travelled > self.board[reward_row][reward_col].travelled and self.board[start_row][start_col].travelled == self.board[start_row][start_col].first_travelled:
                #self.print_board()
                self.my_maze.reassign_weight(rat, start_row, start_col)
                #self.print_board()
                for s in range(30):
                    for t in range(30):
                        if not self.board[s][t].get_weight() == -1 and not self.board[s][t].get_weight() == 1:  # ISSUE HERE
                            if not s == reward_row or not t == reward_col:
                                # self.board[s][t].set_weight(math.log(1/(self.board[s][t].get_weight()),1/(self.board[reward_row][reward_col].get_weight())))
                                self.board[s][t].set_weight(1 / (self.board[s][t].get_weight()))
                        if self.board[s][t].get_weight() >= 1 / (self.board[reward_row][reward_col].get_weight()):
                            self.board[s][t].set_weight(-1)
                self.board[reward_row][reward_col].set_weight(1 / (self.board[reward_row][reward_col].get_weight()))
        self.print_board()
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

        while not math.pow(math.pow(reward_x-rat.get_x(),2)+math.pow(reward_y-rat.get_y(),2),1/2) < 10:
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
                        if not self.is_intersect_wth_gray_cells_new(rat.get_x(),rat.get_y(),x_temp,y_temp):
                            if self.selection_strategy_max:
                                weights.append([self.board[row][col].get_weight(), x_temp,y_temp])
                                weights_map[self.board[row][col].get_weight()] = [x_temp,y_temp]
                            else:
                                rat.move(x_temp,y_temp)
                                break
                        else:
                            config.dl(f"AVOIDED POINT ({x_temp},{y_temp})")
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
                    config.dl(f"TRAPPED IN THE SAME CELL {new_row} {new_col}")
                else:
                    cont_count =0
                if cont_count >= 10:
                    trap_count +=1
                    config.dl(f"TRAP COUNT INCR {trap_count}")
                if trap_count > 2000:
                    return False
                rat.move(b_max[0], b_max[1])
                self.my_maze.damage()
                #print(f"Moving to {b_max[0]},{b_max[1]} {b_max[1]//20} {b_max[0]//20}")
        # update rundata
        self.rundata.num_directions = len(arr)
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
        config.il("")
        # print header
        config.i("{:10} ".format(''))
        for i in range(config.NUMBER_OF_CELLS):
            config.i("{:10.0f} ".format(i))
        config.il("")
        for i in range(config.NUMBER_OF_CELLS):
            config.i("{:10.0f} ".format(i))
            for j in range(config.NUMBER_OF_CELLS):
                config.i(self.board[i][j])
            config.il("")


def main():
    memmap = MemoryModel()
    memmap.init_board()
    memmap.draw_board()
    #print(memmap.is_intersect_wth_gray_cells_new(98.04573113608151,462.197068030155,70.80499047146857,433.13521234090973))

if __name__ == '__main__':
    main()
