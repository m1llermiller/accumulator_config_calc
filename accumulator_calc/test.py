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
        self.Q_pack = num_parallel * cell_dict[cell_name]["Nominal Capacity (Ah)"]  # V
        self.nom_pack_v = num_series * cell_dict[cell_name]["Nominal Voltage (V)"]  # V
        self.max_pack_v = num_series * cell_dict[cell_name]["Max Voltage (V)"]  # V
        self.nom_mod_v = self.nom_pack_v / num_modules  # V
        self.max_mod_v = self.max_pack_v / num_modules  # V
        self.nom_pack_e = self.nom_pack_v * self.Q_pack /1000   # kWh
        self.max_pack_e = self.max_pack_v * self.Q_pack /1000   # kWh
        self.nom_mod_e = self.nom_mod_v * self.Q_pack /1000     # kWh
        self.max_mod_e = self.max_mod_v * self.Q_pack /1000     # kWh
        self.cont_pack_i = num_parallel * cell_dict[cell_name]["Continuous Discharge Current (A)"]  # A
        self.num_cells = num_parallel * num_series
        self.mod_num_cells = self.num_cells / num_modules
        self.cell_mass = self.num_cells * cell_dict[cell_name]["Mass (g)"] / 1000   # kg
        self.mod_cell_mass = self.cell_mass / num_modules   # kg
        self.cell_volume = cell_dict[cell_name]["Volume (L)"] * self.num_cells  # L
        self.mod_volume = self.cell_volume / num_modules    # L

        self.pack_DCIR = ((cell_dict[cell_name]["Typical DCIR (mohm)"]*num_series)/num_parallel)*1000 # Ohms
        p_loss = np.square(self.cont_pack_i) * self.pack_DCIR # This is an approximated power loss when operating at nominal values
        self.nom_power = self.nom_pack_v * self.cont_pack_i
        self.pack_efficiency = (self.nom_power - p_loss) / self.nom_power


        self.data_to_write = [
            self.cell_name,
            self.configuration,
            self.Q_pack,
            self.nom_pack_v,
            self.max_pack_v,
            self.nom_mod_v,
            self.max_mod_v,
            self.nom_pack_e,
            self.max_pack_e,
            self.nom_mod_e,
            self.max_mod_e,
            self.nom_power,
            self.cont_pack_i,
            self.num_cells,
            self.mod_num_cells,
            self.cell_mass,
            self.mod_cell_mass ,
            self.cell_volume,
            self.mod_volume,
            self.pack_DCIR,
            self.pack_efficiency]

    def return_pack_parameters(self):
        '''
        indexes for pack parameters - used when checking externally
        0   cell_name,
        1   pack configuration (series / parallel and number of modules),
        2   pack capacity (Ah),
        3   nominal pack voltage (V),
        4   maximum pack voltage (V),
        5   nominal module voltage (V),
        6   maximum module voltage (V),
        7   nominal pack energy (kWh),
        8   maximum pack energy (kWh),
        9   nominal module energy (kWh),
        10  maximum module energy (kWh),
        11  nominal power output (W) - from nominal voltage and continuous rated current,
        12  continuous rated current (A),
        13  number of cells
        14  number of cells per module,
        15  cell mass (kg),
        16  cell mass per module (kg),
        17  cell volume (L),
        18  cell module volume (L),
        19  pack approx DCIR (ohm),
        20  pack energy efficiency approximation
        '''
        return self.data_to_write # This can be used to check individual parameters externally so invalid layouts can be discarded


    def write_to_dataframe(self):
        # Add row to the output file




