import numpy as np
import pandas as pd
import math

# Load cell selection table
filepath = '21700_cell_options.csv'
df_raw = pd.read_csv(filepath, sep="\t", index_col=0)
df_cells = df_raw.T
cell_dict = df_cells.to_dict(orient="index")


def calc(cell_name, v_target, v_tolerance, e_target_kWh, e_tolerance_kWh):
    cell = cell_dict[cell_name]
    V_cell = np.float64(cell["Maximum Nominal Voltage (V)"])
    Ah_cell = np.float64(cell["Nominal Capacity (Ah)"])

    # Range of acceptable pack voltages
    V_max = v_target + v_tolerance
    V_min = v_target - v_tolerance

    Ns_min = math.ceil(V_min / V_cell)
    Ns_max = math.floor(V_max / V_cell)
    print("Ns min:", Ns_min)
    print("Ns max:", Ns_max)
    Ns_options = np.arange(Ns_min, Ns_max + 1, step=1)

    # Range of acceptable pack energies
    E_max = (e_target_kWh + e_tolerance_kWh) * 1000
    E_min = (e_target_kWh - e_tolerance_kWh) * 1000

    # Power targets in kWh -> required capaicty in Ah -> number of parallel cells required
    Np_min = math.ceil(E_min / (V_max * Ah_cell))
    print("Np min:", Np_min)
    Np_max = math.floor(E_max / (V_min * Ah_cell))
    print("Np max:", Np_max)
    Np_options = np.arange(Np_min, Np_max + 1, step=1)

    # Segment constraint
    segment_options = [4, 5, 6]
    Ns_options = [
        Ns for Ns in Ns_options
        if any(Ns % seg == 0 for seg in segment_options)
    ]

    print("Ns options:", Ns_options)
    print("Np options:", Np_options)

    return Ns_options, Np_options


calc('P45B', 350, 20, 21, 2)
