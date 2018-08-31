import cell
import mouse
import config
import math
import numpy as np
import numpy.linalg
import scipy.stats as sp


class Maze(object):
    def __init__(self,board,matrix,w,T):
        self.board = board
        self.matrix = matrix
        self.w = w
        self.T = T
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

    def reassign_weight(self,mouse,new_row,new_col):
        for i in range (config.NUMBER_OF_CELLS):
            for j in range(config.NUMBER_OF_CELLS):
                self.board[i][j].set_weight(self.board[new_row][new_col].storage[i][j])

    def update_matrix_original(self,x_f,y_f,rat):
        first_index = int(rat.get_y() // 20 * 30 + rat.get_x() // 20)
        second_index = int(y_f // 20 * 30 + x_f // 20)
        if first_index == second_index:
            return
        for c in range(900):
            if c == first_index:
                self.matrix[first_index][c] = self.matrix[first_index][c] + rat.ALPHA * (1 + rat.GAMMA * self.matrix[second_index][c] - self.matrix[first_index][c])
            else:
                self.matrix[first_index][c] = self.matrix[first_index][c] + rat.ALPHA * (0 + rat.GAMMA * self.matrix[second_index][c] - self.matrix[first_index][c])

    def update_matrix(self,x_f,y_f,rat):
        first_index = int(rat.get_y() // 20 * 30 + rat.get_x() // 20)
        second_index = int(y_f // 20 * 30 + x_f // 20)

        if first_index == second_index:
            self.matrix[first_index][first_index] = self.matrix[first_index][first_index] + rat.ALPHA * (1 + rat.GAMMA * self.matrix[second_index][first_index] - self.matrix[first_index][first_index])
        for c in range(900):
            if c != first_index:
                self.matrix[first_index][c] = self.matrix[first_index][c] + rat.ALPHA * (0 + rat.GAMMA * self.matrix[second_index][c] - self.matrix[first_index][c])

    def create_weights_learned(self,mouse,reward_row,reward_col):
        reward_matrix = []
        for f in range (900):
            if f == reward_row*30+reward_col:
                reward_matrix.append(1)
            else:
                reward_matrix.append(-1)
        weights = []
        #self.matrix = self.set_successor(mouse)
        for g in range (900):
            sum = 0
            for h in range (900):
                #sum = 0 bug
                sum += self.matrix[g][h]*reward_matrix[h]
            weights.append(sum)
        # debug
        minus_one_equal = min(weights)
        for i in range(len(weights)):
            weights[i] = weights[i]*-1/minus_one_equal
        config.il(f"MAX VALUE {max(weights)}")
        for x in range (30):
            for y in range (30):
                self.board[x][y].set_weight(weights[30*x+y])


    def set_damage_row(self,row):
        for i in range (900):
            self.matrix[row][i] = 0



    def create_weights_omnicient(self,mouse,reward_row,reward_col):
        reward_matrix = []
        for f in range (900):
            if f == reward_row*30+reward_col:
                reward_matrix.append(1)
            else:
                reward_matrix.append(-1)
        weights = []
        self.matrix = self.set_successor(mouse)
        for g in range (900):
            sum = 0
            for h in range (900):
                #sum = 0 bug
                sum += self.matrix[g][h]*reward_matrix[h]
            weights.append(sum)
        # debug
        minus_one_equal = min(weights)
        for i in range(len(weights)):
            weights[i] = weights[i]*-1/minus_one_equal
        config.il(f"MAX VALUE {max(weights)}")
        for x in range (30):
            for y in range (30):
                self.board[x][y].set_weight(weights[30*x+y])

    def create_T(self,mouse):
        for i in range (900):
            if not self.board[int(i//30)][int(i%30)].is_travellable:
                for j in range (-2,3,1):
                    for k in range (-2,3,1):
                        if int(i // 30)+j >= 0 and int(i // 30)+j <= 29 and int(i % 30)+k >= 0 and int(i % 30)+k <= 29:
                            if not self.board[int(i // 30)+j][int(i % 30)+k].is_travellable:
                                start_row = int(i//30)
                                start_col = int(i % 30)
                                next_row = int(i//30)+ j
                                next_col = int(i % 30) + k
                                p_row = sp.norm.cdf(next_row-start_row+0.5,0,mouse.SIGMA2/(config.CELL_WIDTH)) - sp.norm.cdf(next_row-start_row-0.5,0,mouse.SIGMA2/(config.CELL_WIDTH))
                                p_col = sp.norm.cdf(next_col-start_col+0.5,0,mouse.SIGMA2/(config.CELL_WIDTH)) - sp.norm.cdf(next_col-start_col-0.5,0,mouse.SIGMA2/(config.CELL_WIDTH))
                                p = p_row * p_col
                                if p < 0.001:
                                    p = 0
                                self.T[i][30*(next_row)+(next_col)] = p
                prob_sum = 0
                for m in range (-2,3,1):
                    for n in range (-2,3,1):
                        index_row = int(i//30)
                        index_col = int(i % 30)
                        if index_row+m >= 0 and index_row+m <= 29 and index_col+n >= 0 and index_col+n <= 29:
                            if not self.board[index_row+m][index_col+n].is_travellable:
                                prob_sum += self.T[i][30*(index_row+m)+(index_col+n)]
                if not prob_sum == 0:
                    for s in range (900):
                        self.T[i][s] *= (1/prob_sum)
        total = []
        for b in range (900):
            sum = 0
            for a in range (900):
                sum += self.T[b][a]
            total.append(sum)

        print(total)
        return





    def set_successor(self, mouse):
        i = np.identity(900)
        m_inverse = []
        for d in range (900):
            m_inverse.append([0]*900)
        for p in range (900):
            for q in range (900):
                m_inverse[p][q] = i[p][q]-mouse.GAMMA * self.T[p][q]
        m = numpy.linalg.inv(m_inverse)
        return m




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


    def normpdf(self,x, y, mean, sd):
        var = float(sd) ** 2
        pi = 3.1415926
        denom = (2 * pi * var) ** .5
        num1 = math.exp(-(float(x) - float(mean)) ** 2 / (2 * var))
        num2 = math.exp(-(float(y) - float(mean)) ** 2 / (2 * var))
        return (num1-num2) / denom

