import datetime
import config
import os
class Report(object):


    def __init__(self):
        self.start()

    def start(self):
        self.report(f"------- {datetime.datetime.now()} -------")
        self.report(f"{'fph_mode':<12},"+
                    f"{'damage_mode':<12},"+
                    f"{'lng_length':<12}," +
                    f"{'lng_num_sqrs':<12}," +
                    f"{'lng_time':<12}," +
                    f"{'fph_aborted':<12}," +
                    f"{'fph_sr_lnth':<12}," +
                    f"{'fph_num_trps':<12}," +
                    f"{'fph_num_dmgd':<12}"
                    )

    def report(self,str):
        with open(os.path.join(config.REPORT_FOLDER,"report.csv"), "a+") as f:
            f.write(f"{str}\n")

class ReportData(object):
    def __init__(self,find_path_mode,damage_mode):
        self.find_path_mode = find_path_mode
        self.damage_mode= damage_mode
        self.find_path_num_traps = 0
        self.find_path_search_length = 0
        self.learning_length = 0
        self.learning_time = 0
        self.learning_displacements = 0
        self.learning_num_squares = 0
        self.find_path_aborted = False
        self.find_path_damaged_cell_count=0

    def __str__(self):
        return (f"{self.find_path_mode:<12},"+
                f"{self.damage_mode:<12}," +
                 f"{self.learning_length:>12.3f}," +
                 f"{self.learning_num_squares:>12.0f}," +
                 f"{self.learning_time:>12.0f}," +
                 f"{bool(self.find_path_aborted):<12}," +
                 f"{self.find_path_search_length:>12.3f}," +
                 f"{self.find_path_num_traps:>12.0f}," +
                 f"{self.find_path_damaged_cell_count:>12.0f}")



