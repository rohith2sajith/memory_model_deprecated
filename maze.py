import cell
import mouse
import config
import math
import numpy as np
import numpy.linalg
import scipy.stats as sp
import copy
import time

class Maze(object):
    def __init__(self,memboard,board,matrix,w,T):
        self.memboard = memboard
        self.board = board
        self.matrix = matrix
        self.w = w
        self.T = T
        self.reset_damaging()
        self.snapshot_board = None
        self.snapshot_matrix = None
        self.snapshot_w = None
        self.snapshot_T = None
        self.travelled_cells = []

    def reset_damaging(self):
        self.damage_interval = -1  # no damage
        self.damage_count = 0  # no dmage 1 mean once -1 means forever
        self.damaged_cells = []
        self.cells_to_damage = []
        self.damage_timer = 0
        self.damage_policy_spread = False
        self.damage_mode = config.DAMAGE_MODE_SINGLE_CELL
        self.find_path_mode_regular = False

    def register_travelled_cell(self,row,col):
        if [row,col] not in self.travelled_cells:
            self.travelled_cells.append([row,col])

    def take_snapshot(self):
        """
        Take a snapshot of the data so that we can restore.
        Typically taken after a run
        :return:
        """
        print("..")
        self.snapshot_board = copy.deepcopy(self.board)
        self.snapshot_matrix = copy.deepcopy(self.matrix)
        self.snapshot_T = copy.deepcopy(self.T)
        self.snapshot_w  = copy.deepcopy(self.w)

    def restore_from_snapshot(self):
        print("..")
        if self.snapshot_board:
            self.board = copy.deepcopy(self.snapshot_board)
            self.matrix = copy.deepcopy(self.snapshot_matrix)
            self.T = copy.deepcopy(self.snapshot_T)
            self.w = copy.deepcopy(self.snapshot_w)

    def get_damaged_cell_count(self):
        return len(self.damaged_cells)

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
        for x in range (30):
            for y in range (30):
                self.board[x][y].set_weight(weights[30*x+y])

    def recalculate_weights_learned(self,reward_row,reward_col):
        reward_matrix = []
        for f in range (900):
            if f == reward_row*30+reward_col:
                reward_matrix.append(1)
            else:
                reward_matrix.append(-1)
        weights = []
        for g in range (900):
            sum = 0
            for h in range (900):
                sum += self.matrix[g][h]*reward_matrix[h]
            weights.append(sum)
        minus_one_equal = min(weights)
        for i in range(len(weights)):
            weights[i] = weights[i]*-1/minus_one_equal
        for x in range (30):
            for y in range (30):
                self.board[x][y].set_weight(weights[30*x+y])



    def create_weights_omnicient(self,mouse,reward_row,reward_col):
        reward_matrix = []
        for f in range (900):
            if f == reward_row*30+reward_col:
                reward_matrix.append(1)
            else:
                reward_matrix.append(-1)
        weights = []
        # removed
        # self.matrix = self.set_successor(mouse)
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
        for x in range (30):
            for y in range (30):
                self.board[x][y].set_weight(weights[30*x+y])

    def recalculate_weights(self,omnicient,reward_row,reward_col):
        if self.find_path_mode_regular:
            return
        if omnicient:
            self.recalculate_weights_omnicient(reward_row,reward_col)
        else:
            self.recalculate_weights_learned(reward_row,reward_col)

    def recalculate_weights_omnicient(self,reward_row,reward_col):
        """
        Recalculate weights
        :param reward_row:
        :param reward_col:
        :return:
        """
        t1 = int(round(time.time() * 1000))

        reward_matrix = []
        for f in range (900):
            if f == reward_row*30+reward_col:
                reward_matrix.append(1)
            else:
                reward_matrix.append(-1)
        weights = []
        t2 = int(round(time.time() * 1000))
        for g in range (900):
            sum = 0
            for h in range (900):
                sum += self.matrix[g][h]*reward_matrix[h]
            weights.append(sum)
        # debug
        minus_one_equal = min(weights)
        t3 = int(round(time.time() * 1000))
        for i in range(len(weights)):
            weights[i] = weights[i]*-1/minus_one_equal
        t4 = int(round(time.time() * 1000))
        for x in range (30):
            for y in range (30):
                self.board[x][y].set_weight(weights[30*x+y])
        t5 = int(round(time.time() * 1000))
        print(f"t5-t1: {t5-t1} t2-t1: {t2-t1} t3-t2: {t3-t1} t3-t3: {t4-t3} t5-t4: {t5-t4}")


    def create_T(self,mouse):
        for i in range (900):
            if not self.board[int(i//30)][int(i%30)].is_not_travellable:
                for j in range (-2,3,1):
                    for k in range (-2,3,1):
                        if int(i // 30)+j >= 0 and int(i // 30)+j <= 29 and int(i % 30)+k >= 0 and int(i % 30)+k <= 29:
                            if not self.board[int(i // 30)+j][int(i % 30)+k].is_not_travellable:
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
                            if not self.board[index_row+m][index_col+n].is_not_travellable:
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

    def init_omnicient(self,mouse):
        self.matrix = self.set_successor(mouse)

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
            board[k][0].is_not_travellable = True

        for m in range(19):
            board[29][m + 11].is_not_travellable = True

        board[26][27].is_not_travellable = True
        board[26][28].is_not_travellable = True
        board[26][29].is_not_travellable = True
        board[27][27].is_not_travellable = True
        board[27][28].is_not_travellable = True
        board[27][29].is_not_travellable = True
        board[28][27].is_not_travellable = True
        board[28][28].is_not_travellable = True
        board[28][29].is_not_travellable = True

        for a in range(3):
            for b in range(12):
                board[b + 6][a + 4].is_not_travellable = True

        for a in range(2):
            for b in range(15):
                board[a + 22][b + 4].is_not_travellable = True

        for a in range(5):
            for b in range(8):
                board[b + 15][a + 22].is_not_travellable = True

        for a in range(3):
            for b in range(6):
                board[a + 15][b + 13].is_not_travellable = True

        for a in range(4):
            for b in range(7):
                board[a + 6][b + 13].is_not_travellable = True

        for a in range(1):
            for b in range(7):
                board[a + 6][b + 20].is_not_travellable = True

        for a in range(2):
            for b in range(6):
                board[b][a + 25].is_not_travellable = True

        for a in range(1):
            for b in range(6):
                board[a + 24][b + 4].is_not_travellable = True

        for a in range(2):
            for b in range(3):
                board[a + 21][b + 27].is_not_travellable = True

        for a in range(1):
            for b in range(4):
                board[a + 23][b + 22].is_not_travellable = True

        for a in range(2):
            for b in range(4):
                board[a + 16][b].is_not_travellable = True

        for a in range(2):
            for b in range(3):
                board[b + 18][a].is_not_travellable = True


    def normpdf(self,x, y, mean, sd):
        var = float(sd) ** 2
        pi = 3.1415926
        denom = (2 * pi * var) ** .5
        num1 = math.exp(-(float(x) - float(mean)) ** 2 / (2 * var))
        num2 = math.exp(-(float(y) - float(mean)) ** 2 / (2 * var))
        return (num1-num2) / denom

    def damage_a_cell(self, row,col):
        if self.find_path_mode_regular:
            self.board[row][col].set_weight(0)
        else:
            for i in range (900):
                if i == row*30+col:
                    self.matrix[row*30+col][i] = 1
                else:
                    self.matrix[row*30+col][i] = 0


        # now make the color of the cell to be black
        self.memboard.make_cell_damaged(row,col)
        self.damaged_cells.append([row,col])
        print(f"Damaging cell {row} {col}")

    def not_used_damage_a_cell_and_around_it(self,row,col):
        """
        Damage a cell and around and return the list of cells
        damaged
        :param row:
        :param col:
        :return:
        """
        affected_cells = []
        self.damage_a_cell(row, col)
        affected_cells.append([row,col])
        for a in self.find_adjacent_cells(row,col):
            if a not in self.damaged_cells and a not in affected_cells:
                affected_cells.append(a)
                self.damage_a_cell(row,col)
        return affected_cells


    def a_random_cell(self):
        """
        Return a valid random row and column that is not gray cell
        :return:
        """
        valid_cell = False
        r = None
        while not valid_cell:
            rnd = int(np.random.random()* len(self.travelled_cells))
            r = self.travelled_cells[rnd]
            valid_cell = self.is_valid_damageable_cell(r[0],r[1])
        return r


    def setup_damage(self,find_path_mode_regular,interval,count,damage_mode):
        """

        :param interval: time interval. For each of this interval we will do one or more damage
        :param count:  how many damage -1 means for ever
        :param spread: spread the damage or not
        :param row: you optionalluy specify a row and column
        :param col:
        :return:
        """
        # if we ask to spread the damage then make the count as -1 indicating goes for ever
        if damage_mode == config.DAMAGE_MODE_SPREAD_CELL:
            count = -1
            self.damage_policy_spread = True
        else:
            self.damage_policy_spread = False
        self.find_path_mode_regular = find_path_mode_regular
        self.damage_interval = interval
        self.damage_count = count
        self.damage_timer = 0
        self.damage_mode = damage_mode
        self.damaged_cells.clear()


        # cells_to_damage is an array that container next cell(s) to damage
        # we intiailze with the value given or a random value.
        # when damage() is called we will take from this array and damage it
        # and then add its adjucents cells to this array cells_to_damage
        # and it goes for ever
        self.update_next_damage_cells(True)


    def find_adjacent_cells(self,row,col):
        """
        Find adjacent cells for the given cell. check to see it is valid and not gray
        and return it
        :param row:
        :param col:
        :return:
        """
        cell_list = []
        for i in range(-1,2,1):
            for j in range(-1, 2, 1):
                if i != 0 or j != 0:
                    if row + i >= 0 and row + i <= config.NUMBER_OF_CELLS - 1 and col + j >= 0 and col + j <= config.NUMBER_OF_CELLS - 1:
                        if self.is_valid_damageable_cell(row + i,col + j):
                            cell_list.append([row + i,col + j])

        return cell_list

    def update_next_damage_cells(self,initial):
        """
        Update the next cells to damage
        :return:
        """
        # make a deep copy
        cc = copy.deepcopy(self.cells_to_damage)
        self.cells_to_damage.clear()  # clear array we already damaged it and moved damaged array already

        if self.damage_mode != config.DAMAGE_MODE_SPREAD_CELL:
            r = self.a_random_cell()
            self.cells_to_damage.append(r)
            if self.damage_mode == config.DAMAGE_MODE_ADJ_CELL:
                self.cells_to_damage.extend(self.find_adjacent_cells(r[0],r[1]))
            return
        elif initial:
            r = self.a_random_cell()
            self.cells_to_damage.append(r)
        if initial:
            return

        # for each find adjecent array and add it for next time damage is called
        for r in cc:
            for a in self.find_adjacent_cells(r[0],r[1]):
                if a not in self.damaged_cells and a not in self.cells_to_damage :
                    self.cells_to_damage.append(a)

    def is_valid_damageable_cell(self,row,col):
        """
        A cell is valid and damageable if it is not gray cell and is in the path
        :param row:
        :param col:
        :return:
        """
        return not self.board[row][col].is_not_travellable

    def is_blocked_cell(self,row,col):
        """
        Is the cell a gray cell
        :param row:
        :param col:
        :return:
        """
        return self.board[row][col].is_not_travellable


    def damage(self):
        """
        Damage
        Based on the interval specified it will start the damaging or not
        The self.cells_to_damage list contains next cells to damage. Go through it and damage
        And then find its adjucent cells and add to the list for next iteration
        :return:
        """
        # if already damaged the number of items to damage is done return
        if self.damage_count ==0:
            return False
        damaged = False
        # damage_timer increament every time damage is called and if it is ewual to the intercal damage and reset the counter
        if self.damage_timer == self.damage_interval:
            # damage what ever in the list
            for r in self.cells_to_damage:
                self.damage_a_cell(r[0],r[1])
                damaged = True
            # now add with new ie adjecent for each of them in the list
            self.damage_count -=1
            self.damage_timer = 0
            self.update_next_damage_cells(False)

        else:
            self.damage_timer +=1

        return damaged

