import config

class TrapFinder(object):
    HISTORY_ITEM_LENGTH=4 # no need to change

    def __init__(self,history_length,tolerence_percentage):
        self.history= []
        self.history_coords = [] # to store correpsondinbg coordinates

        self.history_length= history_length
        self.tolerence_percentage = tolerence_percentage

        self.tolerence_count  =  int((self.history_length * self.tolerence_percentage)/100)
        print(f"TOL COUNT={self.tolerence_count}")

    def rewind_to_last_cell(self,current_cell):
        different_cell = False
        cell_id=None
        cell_coords = None
        while not different_cell and len(self.history):
            cell_id = self.history[-1:][0]
            cell_coords = self.history_coords[-1:][0]
            if cell_id == current_cell:
                del self.history[-1:]
                del self.history_coords[-1:]
            else:
                different_cell = True
        return (cell_id,cell_coords)

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
        self.history_coords.append((x,y))

        if self.history.count(cell) >self.tolerence_count:
            # remove the first occureance and return
            #index = self.history.find(cell_id)
            #self.history = self.history[0:index] + self.history[index+self.HISTORY_ITEM_LENGTH:]
            cell_details = self.rewind_to_last_cell(cell)
            return (True,cell_details)
        # trim history if needed
        if len(self.history) > self.history_length:
            self.history.pop(0)

        return (False,None)


def main():
    tf = TrapFinder(30,10)
    for c in [(301,200),(300,201),(200,303),(330,410),(100,200),(100,201),(101,201),(102,202),(103,203)]:
        print(tf.register_visited(c[0],c[1]))
        print(tf.history)
        print(tf.history_coords)
        print()
if __name__ == '__main__':
    main()

