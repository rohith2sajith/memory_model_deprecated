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

    def init_board(self):
        x = 0
        y = 0
        self.board = []
        for row in range(30):
            x = 0
            a_row = []
            for col in range(30):
                # print (f"x:{x} y:{y}")
                x += self.CELL_WIDTH
                # for testing make the is_travelable random
                is_travelable = False

                a_row.append(
                    cell.Cell(self.DEFAULT_WEIGHT, x, y, is_travelable))
            y += self.CELL_WIDTH
            self.board.append(a_row)
        self.my_maze = maze.Maze(self.board)
        self.rat = mouse.Mouse(0,600,0,0,0,self)

    def draw_line(self,x1,y1,x2,y2):
        self.canvas.create_line(x1,y1,x2,y2)

    def move_mouse(self,rat):
        for i in range(10000):#rat.get_v() > rat.MIN:
            #if i == 0:
                #rat.set_a(rat.get_next_acceleration())
            #rat.set_v(rat.get_next_velocity(rat.get_v(),rat.get_a(),rat.get_t()))

            #rat.set_x(rat.get_next_coordinate(rat.get_x(),rat.get_y(),rat.get_v(),rat.get_t())[0])
            #rat.set_y(rat.get_next_coordinate(rat.get_x(), rat.get_y(), rat.get_v(),rat.get_t())[1])

            #coords = rat.get_next_coordinate(rat.get_x(), rat.get_y(), rat.get_v(),
            #                      rat.get_t())
            coords = [0,600]
            coords = rat.get_next_coordinate(rat.get_x(), rat.get_y(), 10,
                                             rat.get_t())

            #while self.board[int(y_f // 20)][int(x_f // 20)].is_travellable:
             #   coords = rat.get_next_coordinate(rat.get_x(), rat.get_y(), 10,
             #                                    rat.get_t())
            x_f =coords[0]
            y_f =coords[1]
            if x_f>580 and x_f<600 and y_f>0 and y_f<20:
                print(x_f,y_f)
                break
            row = int(y_f // 20)
            col = int(x_f // 20)
            if not self.board[int(y_f // 20)][int(x_f // 20)].is_travellable:
                rat.move(x_f,y_f)
                rat.set_t(rat.get_t()+1)

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
