import cell
import mouse
import maze
import tkinter

class MemoryModel (object):
    CELL_WIDTH = 20 # square width
    DEFAULT_WEIGHT =0.1  # default weight
    WALKABLE_CELL_COLOR = "gray"
    BLOCKED_CELL_COLOR = "white"

    def draw_board(self):
        self.root = tkinter.Tk()  # start the gui engine
        self.learning_button = tkinter.Button(self.root, text='START LEARNING',
                                        width=20,
                                        command=self.start_learning)
        self.learning_button.grid(row=0, column=0)
        self.path_button = tkinter.Button(self.root, text='FIND PATH',
                                              width=20,
                                              command=self.find_path)
        self.path_button.grid(row=0, column=2)
        # create canvas

        # you can draw rectangle , lines points etc in a canvas

        self.canvas = tkinter.Canvas(self.root,
                                width=self.CELL_WIDTH * 30,
                                height=self.CELL_WIDTH * 30)
        # pack mean you add show the canvas. By default it will not show
        self.canvas.grid(row=1,column=0)
        # now create rectangle
        for i in range(30):
            for j in range(30):
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
        for row in range(30):
            x = 0
            a_row = []
            for col in range(30):
                # print (f"x:{x} y:{y}")
                # for testing make the is_travelable random
                is_travelable = False
                travelled = -1
                a_row.append(cell.Cell(self.DEFAULT_WEIGHT, x, y, is_travelable, travelled))
                x += 1
            y += 1
            self.board.append(a_row)
        self.my_maze = maze.Maze(self.board)
        self.rat = mouse.Mouse(0,600,0,0,0,self)

    def update_circle(self,id,x,y):
        oldcircle = None
        if id:
            oldcircle = self.canvas.find_withtag(id)
            self.canvas.delete(oldcircle)
        oldcircle =  self.canvas.create_oval(x,y,x+8,y+8,fill="red")
        self.root.update()
        return oldcircle

    def draw_circle_suggested(self,id,delete,x,y):
        oldcircle = None
        if delete:
            oldcircle = self.canvas.find_withtag(id)
            self.canvas.delete(oldcircle)
        else:
            oldcircle =  self.canvas.create_oval(x,y,x+8,y+8,fill="yellow")
            self.root.update()
        return oldcircle

    def draw_line(self,x1,y1,x2,y2):
        last_line = self.canvas.create_line(x1,y1,x2,y2,fill="green")
        self.canvas.itemconfigure(last_line, tags="path")
        self.root.update()

    def move_mouse(self,rat):
        for k in range(1000):#rat.get_v() > rat.MIN:
            #if i == 0:
                #rat.set_a(rat.get_next_acceleration())
            #rat.set_v(rat.get_next_velocity(rat.get_v(),rat.get_a(),rat.get_t()))

            #rat.set_x(rat.get_next_coordinate(rat.get_x(),rat.get_y(),rat.get_v(),rat.get_t())[0])
            #rat.set_y(rat.get_next_coordinate(rat.get_x(), rat.get_y(), rat.get_v(),rat.get_t())[1])

            #coords = rat.get_next_coordinate(rat.get_x(), rat.get_y(), rat.get_v(),
            #                      rat.get_t())
            bool = False
            coords = [0,600]
            while bool is False:
                coords = rat.get_next_coordinate(rat.get_x(), rat.get_y(),
                                             rat.get_t())


                x_f = coords[0]
                y_f = coords[1]
                # draw suggested debug
                # debug
                #old_suggested_circle = self.draw_circle_suggested(None,False,x_f,y_f)
                for  i in range (30):
                    break_loop = False
                    for j in range (30):
                        if self.board[i][j].is_travellable:
                            if rat.intersect(rat.get_x(),rat.get_y(),x_f,y_f,20*j,20*i):
                                bool = False
                                break_loop = True
                                break
                            else:
                                bool = True
                    if break_loop:
                        break

                #self.draw_circle_suggested(old_suggested_circle, True, x_f, y_f)

            #while self.board[int(y_f // 20)][int(x_f // 20)].is_travellable:
             #   coords = rat.get_next_coordinate(rat.get_x(), rat.get_y(), 10,
             #                                    rat.get_t())
            if x_f>580 and x_f<600 and y_f>0 and y_f<20:
                rat.move(x_f,y_f)
                self.board[int(y_f // 20)][int(x_f // 20)].travelled = rat.get_t()
                self.my_maze.update_weight(rat)
                break
            row = int(y_f // 20)
            col = int(x_f // 20)
            if rat.get_t()%100 == 0:
                self.my_maze.update_weight(rat)
            if not self.board[int(y_f // 20)][int(x_f // 20)].is_travellable:
                rat.move(x_f,y_f)
                self.board[int(y_f // 20)][int(x_f // 20)].travelled = rat.get_t()
                rat.set_t(rat.get_t()+1)


    def path(self,rat):
        x_f = rat.get_x()
        y_f = rat.get_y()
        rat.set_x(0)
        rat.set_y(599)
        bool_1 = rat.get_x() > (x_f//20)*20 and rat.get_x()<(x_f//20)*20+20
        bool_2 = rat.get_y() > (y_f//20)*20 and rat.get_y()< (y_f//20)*20+20
        bool_3 = bool_1 and bool_2

        while not bool_3:
            max = -1
            i_max = 0
            j_max = 0
            for i in [-1,1]: #range(-1,2):
                for j in [-1,1]: #range (-1,2):
                    col = rat.get_x()//20
                    row = rat.get_y()//20
                    if (row+i) >= 0 and (row+i) <=29 and (col+j) >= 0 and (col+j) <=29:
                        if self.board[row+i][col+j].get_weight() > max:
                            max = self.board[row+i][col+j].get_weight()
                            i_max = i
                            j_max = j

            rat.move(rat.get_x()+20*j_max, rat.get_y()+20*i_max)

    def print_board(self):
        for i in range(30):
            for j in range(30):
                print(self.board[i][j],end='')
            print()

            # print(rat)
            # instead of setting x and y directly to mouse.
            # call Mouse.move with new points. That will draw the guii

def main():
    memmap = MemoryModel()
    memmap.init_board()
    memmap.draw_board()

    #rat = mouse.Mouse(0,0,0,0,0)

    #while rat.get_v() > rat.MIN:
    #    rat.set_a(rat.get_next_acceleration())
    #    rat.set_v(rat.get_next_velocity(rat.get_v(),rat.get_a(),rat.get_t()))
    #    rat.set_x(rat.get_next_coordinate(rat.get_x(),rat.get_y(),rat.get_v(),rat.get_t())[0])
    #    rat.set_y(rat.get_next_coordinate(rat.get_x(), rat.get_y(), rat.get_v(),rat.get_t())[1])


if __name__ == '__main__':
    main()
