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
        self.cells_to_damage = []
        if self.damage_mode == config.DAMAGE_MODE_SPREAD_CELL:
            self.damage_policy_spread = True
        else:
            self.damage_policy_spread = False
        self.damage_generator = damage_generator


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
                    if row + i >= 0 and row + i <= config.NUMBER_OF_CELLS - 1 and col + j >= 0 and col + j <= config.NUMBER_OF_CELLS - 1:
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

    def get_damagable_cells(self):
        damageble_cells = {}
        self.update_next_damage_cells(True)
        damage_degree = self.damage_generator.get_damage()
        damage_index = self.damage_generator.get_index()

        for di in range(self.damage_count):
            for r in self.cells_to_damage:
                damageble_cells[(r[0],r[1])] = [damage_degree,damage_index]
            # now add with new ie adjecent for each of them in the list
            self.update_next_damage_cells(False)

        return damageble_cells

