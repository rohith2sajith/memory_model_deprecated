import config
import random

class MapEntry(object):
    def __init__(self,x,y,row,col,weight):
        self.row = row
        self.col = col
        self.x = x
        self.y = y
        self.weight = weight
    def __str__(self):
        return f"({self.row},{self.col})"

class MaxWeightPicker(object):
    def __init__(self):
        self.weights_map = {}
        self.black_list = []

    def add_to_black_list(self,row,col):
        self.black_list.append((row,col))

    def clear_black_list(self):
        self.black_list.clear()
    def clear(self):
        self.weights_map.clear()
        #self.clear_black_list()

    def add(self,x,y,weight):
        row = y//config.CELL_WIDTH
        col = x//config.CELL_WIDTH
        entry = MapEntry(x,y,row,col,weight)
        entries = []
        if weight in self.weights_map:
            # if we already have an entry then append to it
            entries = self.weights_map[weight]
        else:
            self.weights_map[weight] = entries
        # append
        entries.append(entry)

    def get_next_coords(self):
        """
        Using max weight strategy get the next coordinates
        By default max weight strategy is to pick coords that has the heighes weight.
        Following are the special cases to handle
        1. If there there more than one cells with weight equal to mx weight then randomly pick on from it
        2. Sometimes because of the trap, we might blak list some cells. In that case do not pick the entries for
           that call. If it turn out to be all cells in max weight is black listed pick the next max one
        :return:
        """
        coords = None
        weight_moving_to =None
        #print(f"Black listed {self.black_list}")
        #for k,v in self.weights_map.items():
        #    print(f"\n{k} -",end='')
        #    for ve in v:
        #        print(ve)
        while not coords and len(self.weights_map):
            max_weight = max(self.weights_map)
            weight_moving_to = max_weight
            entries = self.weights_map[max_weight]
            # remove black listed entries
            if len(self.black_list):
                entries_copy = entries[:]
                for e in entries_copy:
                    if (e.row,e.col) in self.black_list:
                        entries.remove(e)
                # now we have entries removed
            if not len(entries):
                # no more entries in this. So removed
                self.weights_map.pop(max_weight)
            else:
                lucky_entry = random.randint(0,len(entries)-1)
                coords = [entries[lucky_entry].x,entries[lucky_entry].y]
        if not coords:
            print("SOME THING WRONG")
        return (coords,weight_moving_to)
def main():
    m = MaxWeightPicker()
    #m.add_to_black_list(0,2)
    #m.add_to_black_list(0,1)
    for i in [[1,1,1],[21,11,5],[24,11,5],[41,11,2]]:
        m.add(i[0],i[1],i[2])
    print(m.get_next_coords())

if __name__ == '__main__':
    main()