import datetime
import config
class Report(object):


    def __init__(self):
        self.start()

    def start(self):
        self.report(f"------- {datetime.datetime.now()} -------")
        self.report(f"{'fph_mode':<12},{'damage_mode':<12}," +
                    f"{'lng_length':<12},{'lng_num_sqrs':<12}," +
                    f"{'lng_time':<12},{'fph_aborted':<12},{'fph_sr_lnth':<12}," +
                    f"{'fph_num_trps':<12}")

    def report(self,str):
        with open("data.csv", "a+") as f:
            f.write(f"{str}\n")

class ReportData(object):
    def __init__(self,find_path_mode,damage_flag,damage_mode):
        self.find_path_mode = find_path_mode
        if damage_flag:
            if damage_mode == config.DAMAGE_MODE_SINGLE_CELL:
                self.damage_mode = "SINGLE CELL"
            elif damage_mode == config.DAMAGE_MODE_ADJ_CELL:
                self.damage_mode = "ADJ CELL"
            else:
                self.damage_mode = "SPREAD"
        else:
            self.damage_mode = "NO DAMAGING"
        self.damage_mode

        self.find_path_num_traps = 0
        self.find_path_search_length = 0
        self.learning_length = 0
        self.learning_time = 0
        self.learning_displacements = 0
        self.learning_num_squares = 0
        self.find_path_aborted = False

    def __str__(self):
        return f"{self.find_path_mode:<12},{self.damage_mode:<12},{self.learning_length:>12.3f},{self.learning_num_squares:>12.3f},{self.learning_time:>12.3f},{self.find_path_aborted:<12},{self.find_path_search_length:>12.3f},{self.find_path_num_traps:>12.3f}"


