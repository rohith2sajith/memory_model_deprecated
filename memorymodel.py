import cell
import mouse
import maze
import rundata
import report
import config as config
import maze_maker
import max_weight_picker
import utils
import damager
import tkinter
import time
import numpy as np
from sympy import *
from sympy.geometry import *
from sympy.core.numbers import *
import copy
from tkinter import filedialog
from tkinter import IntVar
from tkinter import StringVar
from tkinter import DoubleVar
from datetime import datetime
from operator import itemgetter

import trap_finder

class MemoryModel (object):

    CELL_WIDTH = 20 # square width
    DEFAULT_WEIGHT =0.1  # default weight
    WALKABLE_CELL_COLOR = "white"
    BLOCKED_CELL_COLOR = "gray"
    NUM_DIRECTIONS = 1000


    def __init__(self):
        self.rundata = 1
        self.marking_reward_space = False
        self.reward_start = None
        self.reward_end = None
        self.stop_path_flag = False
        self.reporter = report.Report()
        self.current_maze = config.MAZE_LIST[0]
        self.damage_generator= maze.DamageGeneratorSimple()
        self.damageble_cells_for_this_session = None
        self.damageble_cells_cumulative = {}
        self.running_function=""

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
        stop_button.grid(row=4, column=0)

        mark_goal_button.grid(row=0, column=1)
        analyze_damage_button.grid(row=1,column=1)
        collect_data_button.grid(row=2, column=1)

        return button_group

    def setup_ui_maze_list(self,my_parent):
        maze_list_group = tkinter.LabelFrame(my_parent, text='Maze List',pady=10,padx=10)
        rb1 = tkinter.Radiobutton(maze_list_group, var=self.maze_name_var, text=config.MAZE_LIST[0], value=config.MAZE_LIST[0], command=self.change_maze_handler)
        rb2 = tkinter.Radiobutton(maze_list_group, var=self.maze_name_var, text=config.MAZE_LIST[1], value=config.MAZE_LIST[1], command=self.change_maze_handler)
        rb3 = tkinter.Radiobutton(maze_list_group, var=self.maze_name_var, text=config.MAZE_LIST[2], value=config.MAZE_LIST[2],command=self.change_maze_handler)
        rb4 = tkinter.Radiobutton(maze_list_group, var=self.maze_name_var, text=config.MAZE_LIST[3], value=config.MAZE_LIST[3],command=self.change_maze_handler)
        rb5 = tkinter.Radiobutton(maze_list_group, var=self.maze_name_var, text=config.MAZE_LIST[4], value=config.MAZE_LIST[4], command=self.change_maze_handler)
        rb1.grid(sticky="W", row=0, column=0)
        rb2.grid(sticky="W", row=0, column=1)
        rb3.grid(sticky="W", row=1, column=0)
        rb4.grid(sticky="W", row=1, column=1)
        rb5.grid(sticky="W", row=2, column=0)
        return maze_list_group

    def setup_ui_config_panel(self,my_parent):
        config_panel_group = tkinter.LabelFrame(my_parent, text='RUN CONFIGURATION')

        tkinter.Label(config_panel_group, text='ITERATIONS',width=10).grid(sticky="W",row=0,column=0)
        tkinter.Entry(config_panel_group, width=10,textvar=self.iterations_var).grid(sticky="W",row=0,column=1)
        tkinter.Label(config_panel_group, text='GAMMA',width=10).grid(sticky="W",row=1,column=0)
        tkinter.Entry(config_panel_group, width=10,textvar=self.gamma_var).grid(sticky="W",row=1,column=1)
        tkinter.Label(config_panel_group, text='ALPHA', width=10).grid(sticky="W", row=2, column=0)
        tkinter.Entry(config_panel_group, width=10, textvar=self.alpha_var).grid(sticky="W", row=2, column=1)
        tkinter.Label(config_panel_group, text='GRID SIZE', width=10).grid(sticky="W", row=3, column=0)
        tkinter.Entry(config_panel_group, width=10, textvar=self.grid_size_var).grid(sticky="W", row=3, column=1)
        tkinter.Button(config_panel_group, text='APPLY', width=20, command=self.apply_config_handler).grid(sticky="W", row=3, column=2)
        tkinter.Checkbutton(config_panel_group, text="Use new weight calc",var=self.use_new_weight_calc_var).grid(sticky="W", row=4, column=2)

        return config_panel_group

    def setup_ui_damage_stategy(self,my_parent):
        damage_stategy_group = tkinter.LabelFrame(my_parent, text='Damage Strategy')

        rb1 = tkinter.Radiobutton(damage_stategy_group, var=self.damage_mode_var, text="Single cell every time", value="0")
        rb2 = tkinter.Radiobutton(damage_stategy_group, var=self.damage_mode_var, text="Spread every time", value="1")

        rb1.grid(sticky="W", row=0, column=1)
        rb2.grid(sticky="W", row=1, column=1)

        return damage_stategy_group

    def setup_ui_damage_configuration(self,my_parent):
        damage_group = tkinter.LabelFrame(my_parent, text='DAMAGE CONFIGURATION')
        tkinter.Checkbutton(damage_group, text="Damage", var=self.damage_var).grid(sticky="W",row=0,column=1)
        self.setup_ui_damage_stategy(damage_group).grid(sticky="W",row=1,column=1)

        tkinter.Label(damage_group, text='Damage Count',width=20).grid(sticky="W",row=3,column=0)
        tkinter.Entry(damage_group, width=5, textvariable=self.damage_count_var).grid(sticky="W",row=3,column=1)

        return damage_group

    def create_canvas(self,canvas_frame):
        self.canvas = tkinter.Canvas(canvas_frame,
                                     width=config.CELL_WIDTH * config.NUMBER_OF_CELLS,
                                     height=config.CELL_WIDTH * config.NUMBER_OF_CELLS)
        self.left = tkinter.Canvas(canvas_frame,
                              width=config.CELL_WIDTH,
                              height=config.CELL_WIDTH * config.NUMBER_OF_CELLS)
        self.right = tkinter.Canvas(canvas_frame,
                               width=config.CELL_WIDTH,
                               height=config.CELL_WIDTH * config.NUMBER_OF_CELLS)

        # pack mean you add show the canvas. By default it will not show
        self.left.grid(row=1, column=0)
        self.canvas.grid(row=1, column=1)
        self.right.grid(row=1, column=2)
        self.canvas.bind("<Button-1>", self.on_clicked)

    def resize(self):
        self.canvas.delete("all")
        self.canvas.config( width=config.CELL_WIDTH * config.NUMBER_OF_CELLS,height=config.CELL_WIDTH * config.NUMBER_OF_CELLS)
        self.left.config(width=config.CELL_WIDTH,
                              height=config.CELL_WIDTH * config.NUMBER_OF_CELLS)
        self.right.config( width=config.CELL_WIDTH,
                               height=config.CELL_WIDTH * config.NUMBER_OF_CELLS)
        self.setup_ui_cells()
    def setup_ui_cells(self):
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

    def draw_board(self):
        self.root = tkinter.Tk()  # start the gui engine
        self.strategy_var = IntVar()
        self.iterations_var = StringVar()
        self.damage_var = IntVar()
        self.spread_damage_var = IntVar()
        self.damage_count_var = StringVar()
        self.damage_mode_var = IntVar()
        self.maze_name_var = StringVar()
        self.gamma_var = DoubleVar()
        self.alpha_var = DoubleVar()
        self.grid_size_var = IntVar()
        self.use_new_weight_calc_var = IntVar()

        self.strategy_var.set(1)
        self.damage_var.set(0)
        self.damage_count_var.set("10")
        self.damage_mode_var.set("0")
        self.maze_name_var.set("default")
        self.iterations_var.set(config.num_learning_steps)
        self.gamma_var.set(config.GAMMA)
        self.alpha_var.set(config.ALPHA)
        self.grid_size_var.set(config.NUMBER_OF_CELLS)
        self.use_new_weight_calc_var.set(0)

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
        self.setup_ui_maze_list(self.buttons_frame).grid(row=1, column=0)
        ## Config Panel

        self.setup_ui_buttom_control_panel(self.buttons_frame)

        # Config
        self.setup_ui_config_panel(self.config_frame).grid(row=0,column=0)
        self.setup_ui_damage_configuration(self.config_frame).grid(row=1,column=0)

        ## BOARD CANVASE FRAME
        # you can draw rectangle , lines points etc in a canvas
        self.canvas_frame = tkinter.Frame(self.root)
        self.canvas_frame.grid(row=0, column=1)
        self.create_canvas(self.canvas_frame)

        # now create rectangle
        self.setup_ui_cells()
        #for i in range(config.NUMBER_OF_CELLS):
        #    for j in range(config.NUMBER_OF_CELLS):
        #        cell = self.board()[i][j]
        #        # rectangle need (x1,y1) and x2,y2)
        #        if cell.is_not_travellable:
        #            fill_color = self.BLOCKED_CELL_COLOR
        #       else:
        #            fill_color = self.WALKABLE_CELL_COLOR
        #        box = self.canvas.create_rectangle(self.CELL_WIDTH * j,
        #                                      self.CELL_WIDTH * i,
        #                                      self.CELL_WIDTH * (j + 1),
        #                                      self.CELL_WIDTH * (i + 1),
        #                                      fill=fill_color)
        ## BOTTOM STATUS FRAME
        self.status = tkinter.Label(self.root, text="STATUS:")
        self.status.grid(sticky="W", row=2, column=0, columnspan=2)
        # you need to call this so that the GUI start running


        self.root.mainloop()

    def update_status(self,txt):
        """
        Update status bar
        :param txt:
        :return:
        """
        txt = f"[{self.current_maze}] [{self.running_function}] : {txt}"
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
        config.set_gamma(float(self.gamma_var.get()))
        config.set_alpha(float(self.alpha_var.get()))
        config.set_grid_size(int(self.grid_size_var.get()))
        print(f"GAMMA:{config.GAMMA} ALPHA:{config.ALPHA}")
    def apply_config_handler(self):
        grid_size_changed = False
        if config.NUMBER_OF_CELLS != int(self.grid_size_var.get()):
            grid_size_changed = True
        self.apply_config()
        if grid_size_changed:
            board = maze_maker.MazeBuilder.load_board("default")
            self.my_maze.reinitialize(board)
            self.resize()

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
        self.running_function = "LEARNING"
        self.rundata = rundata.RunData()
        self.apply_config()
        self.my_maze.reset_board_flags()
        self.canvas.delete("path") # remove all paths
        self.move_mouse(self.rat)
        self.print_board()
        # take snapshot of what we leanred
        self.my_maze.take_snapshot()
        self.damageble_cells_for_this_session = None # reset after start leaning
        self.my_maze.save_matrix("ml.csv")

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
                success = self.find_path(n,False,False,0,0,0,0,True)
                if not success:
                    break
                f.write(str(self.rundata) + "\n")
        f.close()
    def update_ui(self,board):
        for row in range(config.NUMBER_OF_CELLS):
            for col in range(config.NUMBER_OF_CELLS):
                x = col * config.CELL_WIDTH + 2
                y = row * config.CELL_WIDTH + 2
                s = self.canvas.find_closest(x, y)
                self.canvas.itemconfig(s, fill=maze_maker.MazeBuilder.get_fill_color(board[row][col].is_not_travellable))

    def change_maze_handler(self):
        self.change_maze(self.maze_name_var.get())

    def change_maze(self,maze_to_load):
        if self.current_maze != maze_to_load:
            print("=== BEFORE CHANGING ===")
            self.print_board()
            # get the damaged cells list and degree first
            board = maze_maker.MazeBuilder.load_board(maze_to_load)
            self.my_maze.reinitialize(board)
            print("=== AFTER CHANGING ===")
            self.print_board()
            # remove unwanter uis
            self.remove_upper_layer()
            self.update_ui(board)
            self.current_maze = maze_to_load
            # update to next
            for c,v in self.damageble_cells_cumulative.items():
                current_damage_index = v[1]
                current_damage_degree = v[0]
                next_damage_index = self.damage_generator.get_next_index(current_damage_index)
                next_damage_degree = self.damage_generator.get_damage(next_damage_index)
                # update
                v[0] = next_damage_degree
                v[1] = next_damage_index

    def analyze_damage_handler(self):
        test_damage_count = 10
        test_count =2
        # for each maze
        for mze in config.MAZE_LIST:
            self.change_maze(mze)  # load the maze
            # do a learning
            self.start_learning()
            # Control
            damage_it = 0 # no damage
            for damage_it in [0,1]:  # with and without damage
                for i in range(test_count): # omnicient
                    self.find_path_omnicient(num_directions=self.NUM_DIRECTIONS,
                                         damage_flag=damage_it, damage_mode=config.DAMAGE_MODE_SINGLE_CELL,
                                          damage_count=test_damage_count)
                    self.update_status("Pausing test for 5 sec...")
                    time.sleep(5)

                for i in range(test_count):  # special path
                    self.find_path_special(num_directions=self.NUM_DIRECTIONS,
                                           damage_flag=damage_it, damage_mode=config.DAMAGE_MODE_SINGLE_CELL,
                                           damage_count=test_damage_count)
                    self.update_status("Pausing test for 5 sec...")
                    time.sleep(5)

    def get_damage_mode_str(self,damage_flag,damage_mode):
        mode = "NO DAMAGING"
        if damage_flag:
            if damage_mode == config.DAMAGE_MODE_SINGLE_CELL:
                mode = "SINGLE CELL"
            else:
                mode = "SPREAD"
        return mode

    def stop_path_handler(self):
        self.stop_path_flag = True
    def remove_upper_layer(self):
        self.canvas.delete("path")
        self.canvas.update()

    def initialize_find_path(self,find_path_mode,damage_flag,damage_mode,damage_count):
        self.update_status("Initializing find path...")
        self.apply_config()
        self.remove_upper_layer()
        self.stop_path_flag = False

        self.reportdata = report.ReportData(find_path_mode, self.get_damage_mode_str(damage_flag,damage_mode))
        if not self.damageble_cells_for_this_session:
            self.damageble_cells_for_this_session = self.generate_damageble_cells(damage_mode,damage_count)
            self.damageble_cells_cumulative.update(self.damageble_cells_for_this_session)

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
        damage_count = int(self.damage_count_var.get())
        use_new_weight_calc = bool(self.use_new_weight_calc_var.get())
        r = self.find_path_omnicient(self.NUM_DIRECTIONS,damage_flag,damage_mode,damage_count,use_new_weight_calc)
        self.my_maze.save_matrix("mo.csv")
        return r

    def find_path_omnicient(self,num_directions,damage_flag,damage_mode,damage_count,use_new_weight_calc):
        self.running_function = "OMNICIENT"
        self.initialize_find_path("OMNICIENT",damage_flag,damage_mode,damage_count)
        r = self.find_path("OMNICIENT",num_directions, True, True,damage_flag,damage_mode,damage_count,use_new_weight_calc)
        self.finalize_find_path()
        return r

    # Find path reguak
    def find_path_handler_regular(self):
        damage_flag = self.damage_var.get()
        damage_mode = int(self.damage_mode_var.get())
        damage_count = int(self.damage_count_var.get())
        use_new_weight_calc = bool(self.use_new_weight_calc_var.get())
        r =  self.find_path_regular(self.NUM_DIRECTIONS,damage_flag,damage_mode,damage_count,use_new_weight_calc)
        return r

    def find_path_regular(self,num_directions,damage_flag,damage_mode,damage_count,use_new_weight_calc):
        self.running_function = "REGULAR"
        self.initialize_find_path("REGULAR",damage_flag,damage_mode,damage_count)
        r = self.find_path("REGULAR",num_directions, False, False,damage_flag,damage_mode,damage_count,use_new_weight_calc)
        self.finalize_find_path()
        return r

    def find_special_path_handler(self):
        damage_flag = self.damage_var.get()
        damage_mode = int(self.damage_mode_var.get())
        damage_count = int(self.damage_count_var.get())
        use_new_weight_calc = bool(self.use_new_weight_calc_var.get())
        r =  self.find_path_special(self.NUM_DIRECTIONS,damage_flag,damage_mode,damage_count,use_new_weight_calc)
        return r

    def find_path_special(self,num_directions,damage_flag,damage_mode,damage_count,use_new_weight_calc):
        self.running_function = "SPECIAL"
        self.initialize_find_path("SPECIAL",damage_flag,damage_mode,damage_count)
        r = self.find_path("SPECIAL",num_directions, True, False,damage_flag,damage_mode,damage_count,use_new_weight_calc)
        self.finalize_find_path()
        return r

    def find_path(self,find_path_mode,num_directions,special,omnicient,damage_flag,damage_mode,damage_count,use_new_weight_calc):
        self.update_status("Restoring from snapshot...")
        self.my_maze.restore_from_snapshot()
        self.update_status("Restoring from snapshot completed")
        return self.path(find_path_mode,self.rat,num_directions,special,omnicient,damage_flag,damage_mode,damage_count,self.damageble_cells_cumulative,use_new_weight_calc)

    def load_maze(self):
        file_path = filedialog.askopenfilename()
        self.my_maze.load(file_path)

    def init_board(self):
        self.my_maze = maze.Maze(self)
        self.my_maze.setup_default_maze()
        self.rat = mouse.Mouse(0, config.BOARD_MAX-1, 0, 0, 0, self)

    def board(self):
        return self.my_maze.board

    def make_cell_damaged(self,row,col,damage_index):
        fill_color = maze_maker.MazeBuilder.get_damage_fill_color(damage_index)
        box = self.canvas.create_rectangle(self.CELL_WIDTH * col,
                                           self.CELL_WIDTH * row,
                                           self.CELL_WIDTH * (col + 1),
                                           self.CELL_WIDTH * (row + 1),
                                           fill=fill_color,tag="path")

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
                        return True
        return False

    def is_intersect_wth_gray_cells(self, rat, new_x, new_y):
        return self.is_intersect_wth_gray_cells_x(rat.get_x(),rat.get_y(),new_x, new_y,self.board())

    def is_intersect_wth_gray_cells_x(self,x1,y1, new_x, new_y,board):
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
                    if board[row][col].is_not_travellable:  # gray cell
                        return True
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
        # use trap finder look for last 50 moves and if the move found 10% match tag it as a trap
        last_time_sigma1_increased = None
        last_visited_row=None
        last_visited_col=None
        continious_visit_count=0
        last_x = None
        last_y = None
        force_to_move_back = False
        visited_tacker = utils.VisitedStack(20)

        while q < config.num_learning_steps:
            # if we have identfied a trap. The best way is to go back
            # to the previous position in last cell and try again
            # high chance of move out of the trap
            cell_to_ignore = None
            if force_to_move_back:
                cell_to_ignore = [last_visited_row,last_visited_row]

            coords = rat.get_next_coor(rat.get_x(), rat.get_y(),cell_to_ignore)

            x_f = coords[0]
            y_f = coords[1]
            if x_f<0 or x_f >=config.BOARD_MAX or y_f<0 or y_f >=config.BOARD_MAX:
                continue


            row = rat.get_y() // config.CELL_WIDTH
            col = rat.get_x()//config.CELL_WIDTH
            # checking to see we have intercepted in non travellable cells
            distance_map = {}

            search_diameter = 2 # neighbourhood search diameter
            for i in range (-1*search_diameter,search_diameter+1,1):
                for j in range (-1*search_diameter,search_diameter+1,1):
                    if row+i >=0 and row+i <=config.NUMBER_OF_CELLS-1 and col+j>=0 and col+j <=config.NUMBER_OF_CELLS-1:
                        if self.board()[int(row+i)][int(col+j)].is_not_travellable:
                            int_arr = rat.intersect2(rat.get_x(), rat.get_y(), x_f, y_f, config.CELL_WIDTH * (col+j), config.CELL_WIDTH *(row+ i))
                            if int_arr[0]:
                                arr = int_arr[1] # array of array of intersection points
                                for cs in arr:
                                    dist = math.sqrt(math.pow(rat.get_x() - cs[0], 2) + math.pow(rat.get_y() - cs[1], 2))
                                    distance_map[dist] = (cs[0], cs[1])

            if len(distance_map):
                right_one = distance_map[min(distance_map)]
                # if there is only one intersection and it is the same as the mouse current locaitons then igre
                if len(distance_map) !=1 or min(distance_map) != 0:
                    x_f = right_one[0]
                    y_f = right_one[1]
                    self.reset_velocity(rat)

            int_arr = rat.intersect_with_grid(rat.get_x(), rat.get_y(),x_f, y_f)
            if int_arr[0]:
                arr = int_arr[1]  # array of array of intersection points
                if len(arr) == 1:
                    x_f = arr[0][0]
                    y_f = arr[0][1]
                    self.reset_velocity(rat)

            row = int(y_f // config.CELL_WIDTH)
            col = int(x_f // config.CELL_WIDTH)
            # Trap unlocking logic
            # sometimes even after asking to ignore the cell for a coordinate
            # when the gray cell intercept is calculated you might end up
            # in the same cell. If the that is the case just send it back
            if force_to_move_back:
                # we are in untrapping mode
                if last_visited_row == row and last_visited_col == col:
                    continue
            force_to_move_back = False
            if rat.get_t()%10 == 0:
                self.my_maze.update_weight(rat)
                zero_distance = sqrt(math.pow(rat.get_x()-0,2)+math.pow(rat.get_y()-(config.BOARD_MAX-1),2))
                displacements.append(zero_distance)

            row = int((y_f)// config.CELL_WIDTH)
            col = int((x_f) // config.CELL_WIDTH)
            # save the mouse coors
            last_mouse_cords = (rat.get_x(), rat.get_y())

            if not self.board()[row][col].is_not_travellable:

                self.my_maze.update_matrix(x_f,y_f,rat)
                self.my_maze.update_w(x_f,y_f,rat)
                # debug
                intersected = 0
                #if debug_number_of_gray_cells_intercted:
                #    intersected=1
                #self.debug_record_move(rat.get_x(),rat.get_y(),x_f,y_f,intersected)

                rat.move(x_f,y_f)
                q +=1
                self.my_maze.register_travelled_cell(row,col)
                self.board()[row][col].travelled = rat.get_t()
                self.my_maze.update_weight(rat)
                self.board()[row][col].first_travelled = rat.get_t()
                for a in range (config.NUMBER_OF_CELLS):
                    for b in range (config.NUMBER_OF_CELLS):
                        self.board()[row][col].storage[a][b] = self.board()[a][b].get_weight()

                rat.set_t(rat.get_t()+1)
                time = time + 1

                # trap tracking -begin
                if last_visited_row == row and last_visited_col == col:
                    # increment count.  Same cell
                    continious_visit_count += 1
                else:
                    # at a different cell
                    continious_visit_count = 0  # reset continuous count
                    # set the last locations
                    last_x = last_mouse_cords[0]
                    last_y = last_mouse_cords[1]
                    visited_tacker.push((last_x,last_y))
                    #print(f"Updating last {last_y//config.CELL_WIDTH}, {last_x//config.CELL_WIDTH}")
                last_visited_row = row
                last_visited_col = col
                # now check we are trapped or not
                if continious_visit_count > 5:
                    continious_visit_count = 0  # reset count
                    force_to_move_back = True  # ask to move back
                    last_safe_cell = (int(last_y // config.CELL_WIDTH), int(last_x // config.CELL_WIDTH))
                # trap section end

            self.update_status(f"Learning:{q:>8}")

        # update for last time
        self.my_maze.update_weight(rat)

        count = 0
        for row in range (config.NUMBER_OF_CELLS):
            for col in range(config.NUMBER_OF_CELLS):
                if self.board()[row][col].weight>0:
                    count = count + 1

        self.rundata.num_squares = count
        self.rundata.learning_length = rat.get_distance()
        self.rundata.displacements = displacements
        self.rundata.time = time
        self.update_status(f"Learning Length: {rat.get_distance():>15.2f}")
        self.reward_end = [rat.get_x(), rat.get_y()]
        print("Adjusting matrics for not visited")
        if 2==1:
            for m in range (config.NUMBER_OF_CELLS_SQR):
                r = m//config.NUMBER_OF_CELLS
                c = m%config.NUMBER_OF_CELLS

                if self.board()[r][c].travelled == -1: # not travelled
                    self.my_maze.matrix[m][m] = 100

    def not_used_isOnLastCell(self,x_f,y_f):
        # check to see the points are on last cell
        return  x_f > config.exit_cell_x1() and x_f < config.exit_cell_x2() and y_f > config.exit_cell_y1() and y_f < config.exit_cell_y2()

    def generate_damageble_cells(self,damage_mode,damage_count):
        dm = damager.DamageManager(self.board(),self.damage_generator,damage_mode,damage_count,self.my_maze.travelled_cells)
        return dm.get_damagable_cells()

    def gen_status_string(self,find_path_mode,loop_count,trap_count):
        str = f"Processing {find_path_mode:>12}..."
        str = f"{str} [{loop_count:>6} traps: {trap_count:>8}"
        str = f"{str} , damaged:{self.my_maze.get_damaged_cell_count():>8}]"
        return str

    def path(self,find_path_mode,rat,num_directions,special,omnicient,damage_flag,damage_mode,damage_count,damageble_cells,use_new_weight_calc):
        reward_row = 10
        reward_col = 10
        if special and omnicient: # initilize
            self.update_status(f"Calculating T ...")
            self.my_maze.create_T(rat)
            self.my_maze.init_omnicient(rat)
        config.il("BOARD BEFORE")
        self.print_board()
        if damage_flag:  # if damage selected
            self.my_maze.damage(damageble_cells)
        else:
            self.my_maze.reset_damaging()

        if special:
            config.il(f" start({self.reward_start[0]},{self.reward_start[1]}) end ({self.reward_end[0]},{self.reward_end[1]})")
            if self.reward_end:
                reward_x = self.reward_end[0]
                reward_y = self.reward_end[1]
                reward_row = reward_y // 20
                reward_col = reward_x // 20
            if omnicient:
                self.update_status(f"Calculating weights ...")
                self.my_maze.create_weights_omnicient(rat,reward_row,reward_col)
                self.update_status(f"Calculating weights completed")
            else:
                self.update_status(f"Calculating weights ...")
                if use_new_weight_calc:
                    self.my_maze.create_weights_learned_new(rat, reward_row, reward_col)
                else:
                    self.my_maze.create_weights_learned(rat, reward_row, reward_col)
                self.update_status(f"Calculating weights completed")
        else:
            reward_x = rat.get_x()
            reward_y = rat.get_y()
            reward_row = reward_y // 20
            reward_col = reward_x // 20
        # damage
        # if damaging needed
        config.il("BOARD AFTER")
        self.print_board()
        # dmage
        learning_distance = rat.get_distance()
        rat.set_distance(0)
        starting_x = 0
        starting_y = config.BOARD_MAX-1
        if special and self.reward_start:
            starting_x = self.reward_start[0]
            starting_y = self.reward_start[1]
            start_row = starting_y // 20
            start_col = starting_x // 20

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
        trap_count_delta=0
        cont_count = 0
        count_trap_count=0
        last_increased_sigma2=None
        trap_details = None
        counter = 0
        # use trap finder look for last 50 moves and if the move found 10% match tag it as a trap
        my_trap_finder = trap_finder.TrapFinder(history_length=50,tolerence_percentage=20)
        loop_count = 0
        pop_count = 0 # used to adjust max weight strategy
        max_entry_picker = max_weight_picker.MaxWeightPicker()

        #while not math.pow(math.pow(reward_x-rat.get_x(),2)+math.pow(reward_y-rat.get_y(),2),1/2) < 10:
        while not(reward_row == rat.get_row() and reward_col == rat.get_col()):
            if self.stop_path_flag:
                break # asked to stop
            loop_count +=1
            self.update_status( self.gen_status_string(find_path_mode,loop_count,trap_count))

            weights.clear()
            arr.clear()
            # max entry picker
            max_entry_picker.clear()
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
                if row >= 0 and row <=(config.NUMBER_OF_CELLS-1) and col >=0 and col<=(config.NUMBER_OF_CELLS-1):
                    r = int(y_f // config.CELL_WIDTH)
                    c = int(x_f // config.CELL_WIDTH)
                    if not self.board()[row][col].is_not_travellable and self.board()[row][col].get_weight() >= self.board()[r][c].get_weight():
                        # if the proposed cell's weight is greater thatn the one already in
                        if not self.is_intersect_wth_gray_cells_new(rat.get_x(),rat.get_y(),x_temp,y_temp):
                            # and not intercepting with non travellable cells add to the weight map
                            weights.append([self.board()[row][col].get_weight(), x_temp,y_temp])
                            weights_map[self.board()[row][col].get_weight()] = [x_temp,y_temp]
                            max_entry_picker.add(x_temp,y_temp,self.board()[row][col].get_weight())
                    else:
                        rat.set_v_x(v_x)
                        rat.set_v_y(v_y)
                else:
                    rat.set_v_x(v_x)
                    rat.set_v_y(v_y)

            if weights_map:
                if 2==1 and trap_details and trap_details[0]:
                    # trapped last time so lets remove one
                    print(f"Untrapping {pop_count}")
                    for ti in range(pop_count):
                        if len(weights_map):
                            weights_map.pop(max(weights_map))
                    if weights_map:
                        b_max = weights_map[max(weights_map)]
                    else:
                        print("#### TRAPPED BUT NO WHERE ELSE TO GO ###")
                else:
                    #b_max = weights_map[max(weights_map)]
                    #print(f"->{max(weights_map)}")
                    b_max,weight_to_move  = max_entry_picker.get_next_coords()
                if b_max:
                    new_row = b_max[1] // 20
                    new_col = b_max[0] // 20
                    prev_row = rat.get_y() // 20
                    prev_col = rat.get_x() // 20
                    # find trap in a new way
                    if new_row == prev_row and new_col == prev_col:
                        cont_count +=1
                        config.dl(f"TRAPPED IN THE SAME CELL {new_row} {new_col}")
                        max_entry_picker.add_to_black_list(new_row,new_col)
                    else:
                        cont_count =0
                        max_entry_picker.clear_black_list()
                    trap_details = my_trap_finder.register_visited(b_max[0], b_max[1])
                    if trap_details[0]:
                        pop_count+=1
                    else:
                        pop_count=0

                    if trap_count > 2000:
                        return False
                    rat.move(b_max[0], b_max[1])
        # update rundata
        self.rundata.num_directions = len(arr)
        self.rundata.num_traps = trap_count
        self.rundata.search_length = rat.get_distance()
        self.update_status(f"find path completed search_length {self.rundata.search_length:>15.2f}")
        return True

    def reset_mouse(self, rat):
        rat.set_x(0)
        rat.set_y(config.BOARD_MAX-1)
        rat.set_v_x(0)
        rat.set_v_y(0)
        for row in range(config.NUMBER_OF_CELLS):
            for col in range(config.NUMBER_OF_CELLS):
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

    def debug_record_move(self,x1,y1,x2,y2,intersected):
        with open("move.csv", 'a+') as move_file:
            move_file.write(f"{x1},{y1},{x2},{y2},{intersected}\n")
            self.debug_check_moves_for_a_move(x1, y1, x2, y2,intersected)

    def debug_check_moves(self):
        rat = mouse.Mouse(0,0,0,0,0,None)
        print("Analyzing Mouse movments")
        with open("move.csv", 'r') as move_file:
            for line in move_file:
                line = line.strip("\n")
                parts = line.split(",")
                x1 = float(parts[0])
                y1 = float(parts[1])
                x2 = float(parts[2])
                y2 = float(parts[3])
                intersection_count = int(parts[4])
                self.debug_check_moves_for_a_move(x1,y1,x2,y2,intersection_count)

    def debug_check_moves_for_a_move(self,x1,y1,x2,y2,intersected):
        rat = mouse.Mouse(0,0,0,0,0,None)
        row = y1//config.CELL_WIDTH
        col = x1//config.CELL_WIDTH
        diameter = 5
        expected_intersection=0
        if intersected:
            expected_intersection=1
        for i in range(-1*diameter, diameter+1, 1):
            for j in range(-1*diameter, diameter+1, 1):
                if row + i >= 0 and row + i <= config.NUMBER_OF_CELLS - 1 and col + j >= 0 and col + j <= config.NUMBER_OF_CELLS - 1:
                    if self.board()[int(row + i)][int(col + j)].is_not_travellable:
                        int_arr = rat.intersect2(x1, y1, x2, y2, config.CELL_WIDTH * (col + j), config.CELL_WIDTH * (row + i))
                        if int_arr[0] and len(int_arr[1])>expected_intersection:
                            print(f"##################({x1},{y1})- ({x2},{y2})) - {int_arr}")

    def debug_analize_point_of_intersection(self):
        rat = mouse.Mouse(0, 0, 0, 0, 0, None)
        p1 = ((138.5719285314413,100.0),(150.81217614351237,92.25987945639311))
        x1 = p1[0][0]
        y1 = p1[0][1]
        x2 = p1[1][0]
        y2 = p1[1][1]
        self.debug_check_moves_for_a_move(x1,y1,x2,y2,True)

def main():
    memmap = MemoryModel()

    memmap.init_board()
    memmap.draw_board()
    #print(memmap.is_intersect_wth_gray_cells_new(98.04573113608151,462.197068030155,70.80499047146857,433.13521234090973))

if __name__ == '__main__':
    main()
