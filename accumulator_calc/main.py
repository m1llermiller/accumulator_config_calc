import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

filepath = '21700_cell_options.csv'

df_raw = pd.read_csv(filepath, sep="\t", index_col=0)
df_cells = df_raw.T
cell_dict = df_cells.to_dict(orient="index") # indexed list of the cell options


cell_name = "M65A"
capacity = cell_dict[cell_name]["Nominal Capacity (Ah)"]
cont_discharge = cell_dict[cell_name]["Continuous Discharge Current (A)"]


class calculate_pack_parameters:
    '''
    This will take in the cell type, and the viable configuration, from this will calculate all required fields to populate a table with the layout

    The easiest approach for writing to the file is to have all the pack parameters laid out in the first line of the csv and for each instance write a new row
    '''

    def __init__(self, V_target, V_tol, E_target, E_tol, cell_name):
        self.V_target = V_target
        self.V_range = [V_target-V_tol, V_target+V_tol]
        self.V_tol = V_tol # Vpack = Vtarget +- Vtol
        self.E_target = E_target
        self.E_range = [E_target-E_tol, E_target+E_tol]
        self.E_tol = E_tol



class pack_layout_config:
    def __init__(self, V_target, V_tol, E_target, E_tol, cell_name):
        self.V_target = V_target
        self.V_range = [V_target-V_tol, V_target+V_tol]
        self.V_tol = V_tol # Vpack = Vtarget +- Vtol
        self.E_target = E_target
        self.E_range = [E_target-E_tol, E_target+E_tol]
        self.E_tol = E_tol

        '''
        For a given cell,
        * nominal voltage target is created and the tolerance on it is defined - defining the potential series configurations
        * energy target is created and the tolerance on it is defined - defining the potential parallel configurations (when also accounting for the series voltage)
        * returns
        * Once a series and parallel number have been determined - the division into cell modules is then calculated
        '''