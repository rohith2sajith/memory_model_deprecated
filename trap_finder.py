import config

class TrapFinder(object):
    HISTORY_ITEM_LENGTH=4 # no need to change

    def __init__(self,history_length,tolerence_percentage):
        self.history= []
        self.history_length= history_length
        self.tolerence_percentage = tolerence_percentage

        self.tolerence_count  =  int((self.history_length * self.tolerence_percentage)/100)
        print(f"TOL COUNT={self.tolerence_count}")

    def rewind_to_last_cell(self,current_cell):
        different_cell = False
        while not different_cell:
            cell_id = self.history[-1:]
            if cell_id == current_cell:
                del self.history[:-1]
            else:
                different_cell = True

    def register_visited(self,x,y):
        """
        Register new visited
        :param row:
        :param col:
        :return:
        """
        row = y // config.CELL_WIDTH
        col = x // config.CELL_WIDTH
        cell = (row,col)
        self.history.append(cell)
        if self.history.count(cell) >self.tolerence_count:
            # remove the first occureance and return
            #index = self.history.find(cell_id)
            #self.history = self.history[0:index] + self.history[index+self.HISTORY_ITEM_LENGTH:]
            self.rewind_to_last_cell(cell)
            return True
        # trim history if needed
        if len(self.history) > self.history_length:
            self.history.pop(0)

        return False


def main():
    tf = TrapFinder(30,10)
    for c in [(8,6),(1,2),(2,3),(3,4),(1,2),(1,2),(1,2),(1,2),(1,2)]:
        print(tf.register_visited(c[0],c[1]))
if __name__ == '__main__':
    main()

