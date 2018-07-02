import cell
import mouse
import config

class Maze(object):
    def __init__(self,board):
        self.board = board
        #self.setup_maze(self.board)

    def update_weight(self,mouse):
        for i in range (config.NUMBER_OF_CELLS):
            for j in range(config.NUMBER_OF_CELLS):
                if j == mouse.get_x()//20 and i == mouse.get_y()//20:
                    self.board[i][j].set_weight(2)
                elif self.board[i][j].travelled == -1:
                    self.board[i][j].set_weight(-1)
                elif self.board[i][j].get_weight()==2:
                    self.board[i][j].set_weight(1/(mouse.get_t()-self.board[i][j].travelled))
                else:
                    #self.board[i][j].set_weight(max(self.board[i][j].get_weight(), 1/(mouse.get_t()-self.board[i][j].travelled)))
                    self.board[i][j].set_weight(1 / (mouse.get_t() - self.board[i][j].travelled))

    def save(self,filename):
        with open(filename,'w') as maz_file:
            for i in range(config.NUMBER_OF_CELLS):
                for j in range(config.NUMBER_OF_CELLS):
                    maz_file.write(self.board[i][j].serialize(i,j))
                    maz_file.write("\n")

    def load(self,filename):
        self.blank_board()
        with open(filename, 'r') as maz_file:
            for line in maz_file:
                line = line.strip("\n")
                my_cell = cell.Cell()
                row,col = my_cell.deserialize(line)

                self.board[row][col] = my_cell

    def blank_board(self):
        x = 0
        y = 0
        self.board = []
        for i in range(config.NUMBER_OF_CELLS):
            a_row = []
            for j in range(config.NUMBER_OF_CELLS):
                a_row.append(cell.Cell(config.DEFAULT_WEIGHT, x, y, False, -1, False))
            self.board.append(a_row)
        return self.board

    def setup_default_maze(self):
        self.setup_with_default_maze(self.board)

    def setup_with_default_maze(self,board):
        for k in range(12):
            board[k][0].is_travellable = True

        for m in range(19):
            board[29][m + 11].is_travellable = True

        board[26][27].is_travellable = True
        board[26][28].is_travellable = True
        board[26][29].is_travellable = True
        board[27][27].is_travellable = True
        board[27][28].is_travellable = True
        board[27][29].is_travellable = True
        board[28][27].is_travellable = True
        board[28][28].is_travellable = True
        board[28][29].is_travellable = True

        for a in range(3):
            for b in range(12):
                board[b + 6][a + 4].is_travellable = True

        for a in range(2):
            for b in range(15):
                board[a + 22][b + 4].is_travellable = True

        for a in range(5):
            for b in range(8):
                board[b + 15][a + 22].is_travellable = True

        for a in range(3):
            for b in range(6):
                board[a + 15][b + 13].is_travellable = True

        for a in range(4):
            for b in range(7):
                board[a + 6][b + 13].is_travellable = True

        for a in range(1):
            for b in range(7):
                board[a + 6][b + 20].is_travellable = True

        for a in range(2):
            for b in range(6):
                board[b][a + 25].is_travellable = True

        for a in range(1):
            for b in range(6):
                board[a + 24][b + 4].is_travellable = True

        for a in range(2):
            for b in range(3):
                board[a + 21][b + 27].is_travellable = True

        for a in range(1):
            for b in range(4):
                board[a + 23][b + 22].is_travellable = True

        for a in range(2):
            for b in range(4):
                board[a + 16][b].is_travellable = True

        for a in range(2):
            for b in range(3):
                board[b + 18][a].is_travellable = True


