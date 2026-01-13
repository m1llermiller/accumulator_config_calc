import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load cell selection table
filepath = '21700_cell_options.csv'
df_raw = pd.read_csv(filepath, sep="\t", index_col=0)
df_cells = df_raw.T
cell_dict = df_cells.to_dict(orient="index")

# Example usecase
cell_name = "M65A"
capacity = cell_dict[cell_name]["Nominal Capacity (Ah)"]
cont_discharge = cell_dict[cell_name]["Continuous Discharge Current (A)"]

# Setup output properties
# This will be another pandas dictionary that the output configurations will be stored in

'''
There will be individual dictionaries for configurations from different cell types

This method means a final check can be passed for all the potential configurations to elimimate potential configurations
against the FSUK criteria 
'''

class FilterConfigurations:
    def __init__(self, config_dict):
        self.config_dict = config_dict # This will contain all potential pack configurations for a given cell type / voltage / energy

    # FSUK specific filtering
    def FSUK_reg_filt(self):
        # Implement checks for number of segments / segment energy /




class Calculate_Pack_Parameters:
    '''
    This will take in the cell type, and the viable configuration, from this will calculate all required fields to populate a table with the layout

    The easiest approach for writing to the file is to have all the pack parameters laid out in the first line of the csv and for each instance write a new row
    '''

    def __init__(self, cell_name, num_series, num_parallel, num_modules, output_file):
        self.cell_name = cell_name
        self.num_series = num_series
        self.num_parallel = num_parallel
        self.num_modules = num_modules
        self.output_file = output_file

        # Calculate pack parameters from inputs
        self.configuration = f'{num_series/num_modules}s{num_parallel}p\t{num_modules}s'
        self.Q_pack = num_parallel * cell_dict[cell_name]["Nominal Capacity (Ah)"]
        self.nom_pack_v = num_series * cell_dict[cell_name]["Nominal Voltage (V)"]
        self.max_pack_v = num_series * cell_dict[cell_name]["Max Voltage (V)"]
        self.nom_mod_v = self.nom_pack_v / num_modules
        self.max_mod_v = self.max_pack_v / num_modules
        self.nom_pack_e =
        self.max_pack_e
        self.nom_mod_e
        self.max_mod_e
        self.max_pack_i
        self.num_cells
        self.mod_num_cells
        self.cell_mass
        self.mod_cell_mass
        self.cell_volume
        self.mod_volume


        self.data_to_write = [self.cell_name, self.configuration, self.Q_pack, self.nom_pack_v, self.max_pack_v, self.nom_mod_v, self.max_mod_v, self.nom_pack_e, self.max_pack_e, self.nom_mod_e, self.max_mod_e, self.max_pack_i, self.num_cells, self.mod_num_cells, self.cell_mass, self.mod_cell_mass ,self.cell_volume, self.mod_volume]

    def return_pack_parameters(self):
        '''
        indexes for pack parameters - used when checking externally
        0 - cell name
        1 - configuration
        2 - pack capacity
        3 - nominal pack voltage
        4 - max pack voltage
        5 - nom mod voltage
        6 - max mod voltage
        7 - nom pack e
        8 - max pack e
        9 - nom mod e
        10 - max mod e
        11 - max pack current
        12 - total number of cells
        13 - number of cells in each module
        14 - mass of all cells
        15 - mass of cells per module
        16 - volume of all cells
        17 - volume of cells per module
        '''
        return self.data_to_write # This can be used to check individual parameters externally so invalid layouts can be discarded


    def save_to_file(self):
        # Add row to the output file




