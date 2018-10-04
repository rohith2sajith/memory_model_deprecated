import config
import copy
import numpy as np

class DamageManager(object):
    def __init__(self,board,damage_generator,damage_mode,damage_count,travelled_cells):
        self.damage_policy_spread = False
        self.damage_count = damage_count
        self.damage_mode = damage_mode
        self.travelled_cells = travelled_cells  # input
        self.board = board

        if self.damage_mode == config.DAMAGE_MODE_SPREAD_CELL:
            self.damage_policy_spread = True
        else:
            self.damage_policy_spread = False
        self.damage_generator = damage_generator
        # storage
        self.cell_to_damage_cumulative_single = {}
        self.cell_to_damage_cumulative_spread = {}

    def is_valid_damageable_cell(self,row,col):
        """
        A cell is valid and damageable if it is not gray cell and is in the path
        :param row:
        :param col:
        :return:
        """
        return not self.board[row][col].is_not_travellable

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
                    if (row + i) >= 0 and (row + i) < config.NUMBER_OF_CELLS and (col + j) >= 0 and (col + j) < config.NUMBER_OF_CELLS:
                        if self.is_valid_damageable_cell(row + i,col + j):
                            cell_list.append([row + i,col + j])
        return cell_list

    def a_random_cell(self):
        """
        Return a valid random row and column that is not gray cell
        :return:
        """
        valid_cell = False
        r = None
        while not valid_cell:
            if self.travelled_cells:
                rnd = int(np.random.random()* len(self.travelled_cells))
                r = self.travelled_cells[rnd]
            else:
                # we did not travel so pick a random value
                row = int(np.random.random()* config.NUMBER_OF_CELLS)
                col = int(np.random.random()* config.NUMBER_OF_CELLS)
                r = [row,col]
            valid_cell = self.is_valid_damageable_cell(r[0],r[1])
        return r

    def update_past_damages(self):
        self._update_past_damages(self.cell_to_damage_cumulative_spread)
        self._update_past_damages(self.cell_to_damage_cumulative_single)

    def _update_past_damages(self,cell_to_damage_cumulative):
        for c, v in cell_to_damage_cumulative.items():
            current_damage_index = v[1]
            current_damage_degree = v[0]
            next_damage_index = self.damage_generator.get_next_index(current_damage_index)
            next_damage_degree = self.damage_generator.get_damage(next_damage_index)
            # update
            v[0] = next_damage_degree
            v[1] = next_damage_index

    def generate_single(self,damage_count,damage_degree, damage_index):
        damageble_cells = {}
        for di in range(damage_count):
            r = self.a_random_cell()
            damageble_cells[(r[0], r[1])] = [damage_degree, damage_index]
        return damageble_cells

    def generate_spread(self,damage_count,damage_degree, damage_index):
        damageble_cells = {}
        if self.cell_to_damage_cumulative_spread:
            # we expand existing
            cc = copy.deepcopy(self.cell_to_damage_cumulative_spread)
            for k, v in cc.items():
                for a in self.find_adjacent_cells(k[0], k[1]):
                    ck = (a[0], a[1])
                    if ck not in damageble_cells and not self.is_already_in_the_list(ck):
                        damageble_cells[ck] = [damage_degree, damage_index]

        else:
            # first time
            for di in range(damage_count):
                r = self.a_random_cell()
                damageble_cells[(r[0], r[1])] = [damage_degree, damage_index]
        return damageble_cells

    def _update_the_list(self,damageble_cells,cell_to_damage_cumulative):
        for k, v in damageble_cells.items():
            if not self.is_already_in_the_list(k):
                cell_to_damage_cumulative[k] = v

    def generate(self):
        """
        Generate and store
        :return:
        """
        self.update_past_damages()
        damageble_cells = {}

        damage_degree = self.damage_generator.get_damage()
        damage_index = self.damage_generator.get_index()

        if self.damage_mode == config.DAMAGE_MODE_SINGLE_CELL:
            # single cell so just add damage_count random cells
            damageble_cells = self.generate_single(self.damage_count,damage_degree, damage_index)
            self._update_the_list(damageble_cells,self.cell_to_damage_cumulative_single)
        elif self.damage_mode == config.DAMAGE_MODE_SPREAD_CELL:
            # spread
            damageble_cells = self.generate_spread(self.damage_count,damage_degree, damage_index)
            self._update_the_list(damageble_cells, self.cell_to_damage_cumulative_spread)
        else: # both
            damage_count_single = self.damage_count//2
            damage_count_spread = self.damage_count - damage_count_single
            # single
            damageble_cells = self.generate_single(damage_count_single, damage_degree, damage_index)
            self._update_the_list(damageble_cells, self.cell_to_damage_cumulative_single)
            # spread
            damageble_cells = self.generate_spread(damage_count_spread, damage_degree, damage_index)
            self._update_the_list(damageble_cells, self.cell_to_damage_cumulative_spread)


    def is_already_in_the_list(self,c):
        return c in self.cell_to_damage_cumulative_single or c in self.cell_to_damage_cumulative_spread

    def get_cells_damage(self):
        cc = copy.deepcopy(self.cell_to_damage_cumulative_single)
        cc.update(self.cell_to_damage_cumulative_spread)
        return cc

    def get_sum_of_damage_degree(self):
        sum = 0
        for k,v in self.get_cells_damage().items():
            sum += (1-v[0])
        return sum

    def get_num_cells_damaged(self):
        return len(self.get_cells_damage())
