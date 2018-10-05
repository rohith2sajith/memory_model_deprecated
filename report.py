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
                    f"{'l_length':<12}," +
                    f"{'l_num_sqrs':<12}," +
                    f"{'l_time':<12}," +
                    f"{'f_aborted':<12}," +
                    f"{'f_sr_lnth':<12}," +
                    f"{'f_num_trps':<12}," +
                    f"{'f_num_dmgd':<12}," +
                    f"{'f_totdm_dgr':<12}," +
                    f"{'f_dmdgr_rio':<12}," +
                    f"{'f_dmcnt_rio':<12}," +
                    f"{'f_dmpth_rio':<12}"
                    )

    def report(self,str):
        with open(os.path.join(config.REPORT_FOLDER,"report.csv"), "a+") as f:
            f.write(f"{str}\n")

class ReportData(object):
    def __init__(self,find_path_mode,damage_flag,damage_mode):
        self.damage_flag = damage_flag
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
        self.sum_of_damage_degrees = 0
        self.num_cells_damaged = 0
        self.total_cells = config.NUMBER_OF_CELLS_SQR
        self.control_path_length=0

    def calculate_damage_degee_ratio(self):
        if self.damage_flag:
            return 1 - (self.sum_of_damage_degrees/self.total_cells)
        return 0

    def calculate_damage_count_ratio(self):
        if self.damage_flag and self.total_cells:
            return 1 - (self.num_cells_damaged/self.total_cells)
        return  0

    def calculate_path_ratio(self):
        if self.damage_flag and self.control_path_length:
            return self.find_path_search_length/self.control_path_length
        return 0

    def __str__(self):
        fph_dmg_dgr_rio = self.calculate_damage_degee_ratio()
        fph_dmg_cnt_rio = self.calculate_damage_count_ratio()
        fph_dmg_pth_rio = self.calculate_path_ratio()

        return (f"{self.find_path_mode:<12},"+
                f"{self.damage_mode:<12}," +
                 f"{self.learning_length:>12.3f}," +
                 f"{self.learning_num_squares:>12.0f}," +
                 f"{self.learning_time:>12.0f}," +
                 f"{bool(self.find_path_aborted):<12}," +
                 f"{self.find_path_search_length:>12.3f}," +
                 f"{self.find_path_num_traps:>12.0f}," +
                 f"{self.find_path_damaged_cell_count:>12.0f},"+
                 f"{self.sum_of_damage_degrees:>12.5f}," +
                 f"{fph_dmg_dgr_rio:>12.5f}," +
                 f"{fph_dmg_cnt_rio:>12.5f}," +
                 f"{fph_dmg_pth_rio:>12.5f}"
                )



