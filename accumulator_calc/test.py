import numpy as np
import pandas as pd

# Load cell selection table
filepath = '21700_cell_options.csv'
df_raw = pd.read_csv(filepath, sep="\t", index_col=0)
df_cells = df_raw.T
cell_dict = df_cells.to_dict(orient="index")


V_target = 350 # Target specified in terms of nominal pack voltage
V_tolerance = 25
P_taget = 25 #kWh
P_tolerance = 3 #kWh

def calc(cell_name, v_target, v_tolerance, p_target, p_tolerance):
    # Calculate the number in series
    V_max, V_min = (v_target + v_tolerance), (v_target - v_tolerance)
    cell_dict[cell_name]["Nominal Voltage (V)"]

    min_ser = V_target

    # Calls the functions previously outlined