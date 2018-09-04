import cell
import mouse
import maze
import rundata
import report
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
        self.stop_path_flag = False
        self.reporter = report.Report()

    def setup_ui_buttom_control_panel(self,my_parent):
        button_group = tkinter.LabelFrame(my_parent, text='CONTROL PANEL',pady=10,padx=10)
        learning_button = tkinter.Button(button_group, text='START LEARNING',width=20,command=self.start_learning)

        path_button = tkinter.Button(button_group, text='FIND PATH', width=20, command=self.find_path_handler_regular)

        collect_data_button = tkinter.Button(button_group, text='COLLECT DATA',width=20,command=self.collect_data)
        special_path_button = tkinter.Button(button_group, text='SPECIAL PATH',width=20,command=self.find_special_path_handler)
        mark_goal_button = tkinter.Button(button_group, text='SELECT REWARD SPACE',width=20,command=self.start_marking_reward_handler)
        omnicient_button = tkinter.Button(button_group, text='OMNICIENT SUCCESSOR',width=20,command=self.find_path_handler_omnicient)
        analyze_damage_button = tkinter.Button(button_group, text='ANALYZE DAMAGE',width=20,command=self.analyze_damage_handler)
        stop_button = tkinter.Button(button_group, text='STOP PATH',width=20,command=self.stop_path_handler)
        learning_button.grid(row=0, column=0)
        path_button.grid(row=1, column=0)
        special_path_button.grid(row=2, column=0)
        omnicient_button.grid(row=3, column=0)
        mark_goal_button.grid(row=4, column=0)
        analyze_damage_button.grid(row=5,column=0)
        collect_data_button.grid(row=6, column=0)
        stop_button.grid(row=7, column=0)

        return button_group


    def setup_ui_config_panel(self,my_parent):
        config_panel_group = tkinter.LabelFrame(my_parent, text='RUN CONFIGURATION')

        iteration_label = tkinter.Label(config_panel_group, text='ITERATIONS',width=10)
        self.iterations = tkinter.Entry(config_panel_group, width=10,textvar=self.iterations_var)
        strategy_chk = tkinter.Checkbutton(config_panel_group,text="Max weight strategy", var = self.strategy_var)
        avoid_gray_chk = tkinter.Checkbutton(config_panel_group, text="Avoid gray", var=self.avoid_gray)

        iteration_label.grid(sticky="W",row=0,column=0)
        self.iterations.grid(sticky="W",row=0,column=1)
        strategy_chk.grid(sticky="W",row=1,column=1)
        avoid_gray_chk.grid(sticky="W",row=2, column=1)
        return config_panel_group

    def setup_ui_damage_stategy(self,my_parent):
        damage_stategy_group = tkinter.LabelFrame(my_parent, text='Damage Strategy')

        rb1 = tkinter.Radiobutton(damage_stategy_group, var=self.damage_mode_var, text="Single cell every time", value="0")
        rb2 = tkinter.Radiobutton(damage_stategy_group, var=self.damage_mode_var, text="Adj cell every time", value="1")
        rb3 = tkinter.Radiobutton(damage_stategy_group, var=self.damage_mode_var, text="Spread every time", value="2")

        rb1.grid(sticky="W", row=0, column=1)
        rb2.grid(sticky="W", row=1, column=1)
        rb3.grid(sticky="W", row=2, column=1)

        return damage_stategy_group

    def setup_ui_damage_configuration(self,my_parent):
        damage_group = tkinter.LabelFrame(my_parent, text='DAMAGE CONFIGURATION')
        tkinter.Checkbutton(damage_group, text="Damage", var=self.damage_var).grid(sticky="W",row=0,column=1)
        self.setup_ui_damage_stategy(damage_group).grid(sticky="W",row=1,column=1)

        tkinter.Label(damage_group, text='Damage Interval',width=20).grid(sticky="W",row=2,column=0)
        tkinter.Entry(damage_group, width=5, textvariable=self.damage_interval_var).grid(sticky="W",row=2,column=1)

        tkinter.Label(damage_group, text='Damage Count',width=20).grid(sticky="W",row=3,column=0)
        tkinter.Entry(damage_group, width=5, textvariable=self.damage_count_var).grid(sticky="W",row=3,column=1)

        return damage_group


    def draw_board(self):
        self.root = tkinter.Tk()  # start the gui engine
        self.strategy_var = IntVar()
        self.avoid_gray  = IntVar()
        self.damage_interval_var = StringVar()
        self.iterations_var = StringVar()
        self.damage_var = IntVar()
        self.spread_damage_var = IntVar()
        self.damage_count_var = StringVar()
        self.damage_mode_var = IntVar()

        self.avoid_gray.set(1)
        self.strategy_var.set(1)
        self.damage_var.set(1)
        self.damage_interval_var.set("10")
        self.damage_count_var.set("10")
        self.damage_mode_var.set("1")
        self.iterations_var.set(config.num_learning_steps)

        ## TOP CONTROL BUTTON FRAME
        self.top_frame = tkinter.Frame(self.root)
        self.top_frame.grid(row=0, column=0)
        ###   TOP FRAME ####
        self.buttons_frame = tkinter.Frame(self.top_frame)
        self.config_frame = tkinter.Frame(self.top_frame)
        self.buttons_frame.grid(row=0,column=0)
        self.config_frame.grid(row=1, column=0)

        # Control Panel
        self.setup_ui_buttom_control_panel(self.buttons_frame).grid(row=0,column=0)
        ## Config Panel

        self.setup_ui_buttom_control_panel(self.buttons_frame)

        # Config
        self.setup_ui_config_panel(self.config_frame).grid(row=0,column=0)
        self.setup_ui_damage_configuration(self.config_frame).grid(row=1,column=0)

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
        self.status.grid(sticky="W",row=2, column=0,columnspan=2)

        # now create rectangle
        for i in range(config.NUMBER_OF_CELLS):
            for j in range(config.NUMBER_OF_CELLS):
                cell = self.board()[i][j]
                # rectangle need (x1,y1) and x2,y2)
                if cell.is_not_travellable:
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
        config.num_learning_steps=int(self.iterations_var.get())

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
        # take snapshot of what we leanred
        self.my_maze.take_snapshot()

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
                success = self.find_path(n,False,False,0,0,0,0)
                if not success:
                    break
                f.write(str(self.rundata) + "\n")
        f.close()

    def analyze_damage_handler(self):
        for i in range(100):
            self.start_learning()
            # find regulat path
            self.find_path_regular(self.NUM_DIRECTIONS,0,0,0,0)
            self.find_path_special(self.NUM_DIRECTIONS,0,0,0,0)
            self.find_path_omnicient(self.NUM_DIRECTIONS,0,0,0,0)

            for damage_interval in [10,20,50,75]:
                # single cell
                self.find_path_regular(self.NUM_DIRECTIONS, 1, 0, damage_interval, -1)
                self.find_path_special(self.NUM_DIRECTIONS, 1, 0, damage_interval, -1)
                self.find_path_omnicient(self.NUM_DIRECTIONS, 1, 0, damage_interval, -1)

                self.find_path_regular(self.NUM_DIRECTIONS, 1, 1, damage_interval, -1)
                self.find_path_special(self.NUM_DIRECTIONS, 1, 1, damage_interval, -1)
                self.find_path_omnicient(self.NUM_DIRECTIONS, 1, 1, damage_interval, -1)

                self.find_path_regular(self.NUM_DIRECTIONS, 1, 2, damage_interval, -1)
                self.find_path_special(self.NUM_DIRECTIONS, 1, 2, damage_interval, -1)
                self.find_path_omnicient(self.NUM_DIRECTIONS, 1, 2, damage_interval, -1)

    def get_damage_mode_str(self,damage_flag,damage_mode):
        mode = "NO DAMAGING"
        if damage_flag:
            if damage_mode == config.DAMAGE_MODE_SINGLE_CELL:
                mode = "SINGLE CELL"
            elif damage_mode == config.DAMAGE_MODE_ADJ_CELL:
                mode = "ADJ CELL"
            else:
                mode = "SPREAD"
        return mode

    def stop_path_handler(self):
        self.stop_path_flag = True

    def initialize_find_path(self,find_path_mode,damage_flag,damage_mode):
        self.selection_strategy_max = bool(self.strategy_var.get())
        self.apply_config()
        self.canvas.delete("path")
        self.canvas.update()
        self.stop_path_flag = False

        self.reportdata = report.ReportData(find_path_mode, self.get_damage_mode_str(damage_flag,damage_mode))

    def finalize_find_path(self):
        self.reportdata.learning_length = self.rundata.learning_length
        self.reportdata.find_path_num_traps  = self.rundata.num_traps
        self.reportdata.find_path_search_length = self.rundata.search_length
        self.reportdata.learning_displacements = self.rundata.displacements
        self.reportdata.learning_num_squares = self.rundata.num_squares
        self.reportdata.learning_time  = self.rundata.time
        self.reportdata.find_path_aborted = self.stop_path_flag
        self.reportdata.find_path_damaged_cell_count = self.my_maze.get_damaged_cell_count()
        self.reporter.report(self.reportdata)

    def find_path_handler_omnicient(self):
        damage_flag = self.damage_var.get()
        damage_mode = int(self.damage_mode_var.get())
        damage_interval = int(self.damage_interval_var.get())
        damage_count = int(self.damage_count_var.get())
        r = self.find_path_omnicient(self.NUM_DIRECTIONS,damage_flag,damage_mode,damage_interval,damage_count)
        return r

    def find_path_omnicient(self,num_directions,damage_flag,damage_mode,damage_interval,damage_count):
        self.initialize_find_path("OMNICIENT",damage_flag,damage_mode)
        r = self.find_path("OMNICIENT",num_directions, True, True,damage_flag,damage_mode,damage_interval,damage_count)
        self.finalize_find_path()
        return r

    # Find path reguak
    def find_path_handler_regular(self):
        damage_flag = self.damage_var.get()
        damage_mode = int(self.damage_mode_var.get())
        damage_interval = int(self.damage_interval_var.get())
        damage_count = int(self.damage_count_var.get())

        r =  self.find_path_regular(self.NUM_DIRECTIONS,damage_flag,damage_mode,damage_interval,damage_count)
        return r

    def find_path_regular(self,num_directions,damage_flag,damage_mode,damage_interval,damage_count):
        self.initialize_find_path("REGULAR",damage_flag,damage_mode)
        r = self.find_path("REGULAR",num_directions, False, False,damage_flag,damage_mode,damage_interval,damage_count)
        self.finalize_find_path()
        return r

    def find_special_path_handler(self):
        damage_flag = self.damage_var.get()
        damage_mode = int(self.damage_mode_var.get())
        damage_interval = int(self.damage_interval_var.get())
        damage_count = int(self.damage_count_var.get())

        r =  self.find_path_special(self.NUM_DIRECTIONS,damage_flag,damage_mode,damage_interval,damage_count)
        return r

    def find_path_special(self,num_directions,damage_flag,damage_mode,damage_interval,damage_count):
        self.initialize_find_path("SPECIAL",damage_flag,damage_mode)
        r = self.find_path("SPECIAL",num_directions, True, False,damage_flag,damage_mode,damage_interval,damage_count)
        self.finalize_find_path()
        return r

    def find_path(self,find_path_mode,num_directions,special,omnicient,damage_flag,damage_mode,damage_interval,damage_count):
        self.update_status("Restoring from snapshot...")
        self.my_maze.restore_from_snapshot()
        self.update_status("Restoring from snapshot completed")
        return self.path(find_path_mode,self.rat,num_directions,special,omnicient,damage_flag,damage_mode,damage_interval,damage_count)

    def load_maze(self):
        file_path = filedialog.askopenfilename()
        self.my_maze.load(file_path)

    def init_board(self):
        x = 0
        y = 0
        board = []
        #
        # initialize the board with cells
        #

        for row in range(config.NUMBER_OF_CELLS):
            x = 0
            a_row = []
            for col in range(config.NUMBER_OF_CELLS):
                # print (f"x:{x} y:{y}")
                # for testing make the is_travelable random
                is_not_travellable = False
                travelled = -1
                first_travelled = -1
                traced = False
                a_row.append(cell.Cell(self.DEFAULT_WEIGHT, x, y, is_not_travellable, travelled, first_travelled, traced))
                x += 1
            y += 1
            board.append(a_row)
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
        self.my_maze = maze.Maze(self,board, self.matrix, w,T)
        self.my_maze.setup_default_maze()

        self.rat = mouse.Mouse(0,599,0,0,0,self)

    def board(self):
        return self.my_maze.board

    def make_cell_damaged(self,row,col):

        box = self.canvas.create_rectangle(self.CELL_WIDTH * col,
                                           self.CELL_WIDTH * row,
                                           self.CELL_WIDTH * (col + 1),
                                           self.CELL_WIDTH * (row + 1),
                                           fill="black",tag="path")

        x = col*config.CELL_WIDTH+2
        y = row*config.CELL_WIDTH+2
        c = self.canvas.find_closest(x,y)
        self.canvas.itemconfig(c, fill="black")
        ##self.canvas.update()

    def update_circle(self,id,x,y):
        oldcircle = None
        if id:
            oldcircle = self.canvas.find_withtag(id)
            self.canvas.delete(oldcircle)
        oldcircle =  self.canvas.create_oval(x,y,x+config.MOUSE_RADIUS,
                                             y+config.MOUSE_RADIUS,
                                             fill=config.MOUSE_FILL_COLOR, tag="path")
        self.canvas.update()
        return oldcircle

    def draw_line(self,x1,y1,x2,y2):
        last_line = self.canvas.create_line(x1,y1,x2,y2,fill=config.PATH_LINE_COLOR, width=2)
        self.canvas.itemconfigure(last_line, tags="path")
        ##self.root.update()

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
                if self.board()[row][col].is_not_travellable:
                    lower_x = config.CELL_WIDTH * col
                    lower_y = config.CELL_WIDTH * row
                    arr = mouse.Mouse.intersect2(x1, y1, new_x, new_y, lower_x, lower_y)
                    if arr[0]:
                        config.dl(f"AVOIDING ({new_x},{new_y})")
                        return True
        return False

    def is_intersect_wth_gray_cells(self, rat, new_x, new_y):
        return self.is_intersect_wth_gray_cells_x(rat.get_x(),rat.get_y(),new_x, new_y,bool(self.avoid_gray.get()),self.board())

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
                    if board[row][col].is_not_travellable:  # gray cell
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
        q = 0
        while q < config.num_learning_steps:
        #for q in range (config.num_learning_steps):
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
                        if self.board()[int(row+i)][int(col+j)].is_not_travellable:
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
                #self.board()[int((y_f-0.00001) // config.CELL_WIDTH)][int((x_f-0.00001) //config.CELL_WIDTH)].travelled = rat.get_t()
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
            if not self.board()[row][col].is_not_travellable:
                #self.my_maze.update_weight(rat)
                self.my_maze.update_matrix(x_f,y_f,rat)

                rat.move(x_f,y_f)
                q +=1
                self.my_maze.register_travelled_cell(row,col)
                self.board()[row][col].travelled = rat.get_t()
                self.my_maze.update_weight(rat)
                self.board()[row][col].first_travelled = rat.get_t()
                for a in range (30):
                    for b in range (30):
                        self.board()[row][col].storage[a][b] = self.board()[a][b].get_weight()

                rat.set_t(rat.get_t()+1)
                time = time + 1
            self.update_status(f"Learning:{q:>8}")

        # update for last time
        self.my_maze.update_weight(rat)
        count = 0
        for row in range (30):
            for col in range(30):
                if self.board()[row][col].weight>0:
                    count = count + 1
        self.rundata.num_squares = count
        self.rundata.learning_length = rat.get_distance()
        self.rundata.displacements = displacements
        self.rundata.time = time
        self.update_status(f"Learning Length: {rat.get_distance():>15.2f}")
        self.reward_end = [rat.get_x(), rat.get_y()]

    def isOnLastCell(self,x_f,y_f):
        # check to see the points are on last cell
        return  x_f > config.exit_cell_x1() and x_f < config.exit_cell_x2() and y_f > config.exit_cell_y1() and y_f < config.exit_cell_y2()

    def path(self,find_path_mode,rat,num_directions,special,omnicient,damage_flag,damage_mode,damage_interval,damage_count):

        # if damaging needed
        if damage_flag:  # if damage selected
            mode_regular = False
            if find_path_mode == "REGULAR":
                mode_regular = True
            self.my_maze.setup_damage(find_path_mode_regular=mode_regular,interval=damage_interval,count=damage_count,damage_mode=damage_mode) # setup the damaging
        else:
            self.my_maze.reset_damaging()

        reward_row = 10
        reward_col = 10

        if special:
            config.il(f" start({self.reward_start[0]},{self.reward_start[1]}) end ({self.reward_end[0]},{self.reward_end[1]})")
            if self.reward_end:
                reward_x = self.reward_end[0]
                reward_y = self.reward_end[1]
                reward_row = reward_y // 20
                reward_col = reward_x // 20
            if omnicient:
                self.update_status(f"Calculating T ...")
                self.my_maze.create_T(rat)
                self.update_status(f"Calculating weights ...")
                self.my_maze.create_weights_omnicient(rat,reward_row,reward_col)
                self.update_status(f"Calculating weights completed")
        else:
            reward_x = rat.get_x()
            reward_y = rat.get_y()
            reward_row = reward_y // 20
            reward_col = reward_x // 20

        learning_distance = rat.get_distance()
        rat.set_distance(0)
        starting_x = 0
        starting_y = 599
        if special and self.reward_start:
            starting_x = self.reward_start[0]
            starting_y = self.reward_start[1]
            start_row = starting_y // 20
            start_col = starting_x // 20

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

        loop_count = 0
        while not math.pow(math.pow(reward_x-rat.get_x(),2)+math.pow(reward_y-rat.get_y(),2),1/2) < 10:
            if self.stop_path_flag:
                break # asked to stop
            loop_count +=1
            self.update_status(f"Processing {find_path_mode:>12}... [{loop_count:>6} traps: {trap_count:>8}, damaged:{self.my_maze.get_damaged_cell_count():>8}]")
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
                    w = self.board()[row][col].get_weight()
                    tr = y_f//config.CELL_WIDTH
                    tc = x_f//config.CELL_WIDTH
                    w1 = self.board()[int(y_f//config.CELL_WIDTH)][int(x_f//config.CELL_WIDTH)].get_weight()
                    if not self.board()[row][col].is_not_travellable and self.board()[row][col].get_weight() >= self.board()[int(y_f // config.CELL_WIDTH)][int(x_f // config.CELL_WIDTH)].get_weight():
                        if not self.is_intersect_wth_gray_cells_new(rat.get_x(),rat.get_y(),x_temp,y_temp):
                            if self.selection_strategy_max:
                                weights.append([self.board()[row][col].get_weight(), x_temp,y_temp])
                                weights_map[self.board()[row][col].get_weight()] = [x_temp,y_temp]
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
                if self.my_maze.damage():  # if we are askewd to damage then recalulate
                    self.update_status(f"[{loop_count}] Recalculating weights...")
                    self.my_maze.recalculate_weights(omnicient,reward_row,reward_col)
                    self.update_status(f"[{loop_count}] Recalculating weights completed")
                #print(f"Moving to {b_max[0]},{b_max[1]} {b_max[1]//20} {b_max[0]//20}")
        # update rundata
        self.rundata.num_directions = len(arr)
        self.rundata.num_traps = trap_count
        self.rundata.search_length = rat.get_distance()
        self.update_status(f"find path completed search_length {self.rundata.search_length:>15.2f}")
        return True

    def reset_mouse(self, rat):
        rat.set_x(0)
        rat.set_y(599)
        rat.set_v_x(0)
        rat.set_v_y(0)
        for row in range(30):
            for col in range(30):
                self.board()[row][col].set_weight(-1)
                self.board()[row][col].travelled = -1
                self.board()[row][col].traced = False

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
                config.i(self.board()[i][j])
            config.il("")


def main():
    memmap = MemoryModel()
    memmap.init_board()
    memmap.draw_board()
    #print(memmap.is_intersect_wth_gray_cells_new(98.04573113608151,462.197068030155,70.80499047146857,433.13521234090973))

if __name__ == '__main__':
    main()
