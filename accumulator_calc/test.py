import numpy as np
import pandas as pd
import math

# Load cell selection table
filepath = '21700_cell_options.csv'
df_raw = pd.read_csv(filepath, sep=",", index_col=0)
df_cells = df_raw.T
cell_dict = df_cells.to_dict(orient="index")


def calc(cell_name, v_target, v_tolerance, e_target_kWh, e_tolerance_kWh):
    potential_configs = [] # To be populated by (num_series, num_parallel, num_segments)

    cell = cell_dict[cell_name]
    V_cell = np.float64(cell["Nominal Voltage (V)"])
    Ah_cell = np.float64(cell["Nominal Capacity (Ah)"])

    # Range of acceptable pack voltages
    V_max = v_target + v_tolerance
    V_min = v_target - v_tolerance

    Ns_min = math.ceil(V_min / V_cell)
    Ns_max = math.floor(V_max / V_cell)

    # test to see how this impacts the pack voltages
    V_max_pack = Ns_max * V_cell
    V_min_pack = Ns_min * V_cell

    # Range of acceptable series cell configurations
    Ns_options = np.arange(Ns_min, Ns_max + 1, step=1)

    # only designing for packs with between 4 and 7 segments
    segment_options = [4, 5, 6, 7]

    # Keep only the series combinations that permit division into equal cell segments
    Ns_options = [Ns for Ns in Ns_options if any(Ns % seg == 0 for seg in segment_options)]

    # Finding the subsequent required parallel cells to build to the desired capacity

    # Range of acceptable pack energies
    E_max = (e_target_kWh + e_tolerance_kWh) * 1000 # Wh
    E_min = (e_target_kWh - e_tolerance_kWh) * 1000 # Wh

    print(f'Enegry targets: E_max = {E_max}kWh, E_min = {E_min}kWh')

    # to generate the parallel cell combinations
    for Ns in Ns_options:
        for seg in segment_options:
            if Ns % seg == 0:
                print(f'V_cell = {V_cell}, Ah_cell = {Ah_cell}, Ns = {Ns}, pack_voltage = {Ns*V_cell}')
                print(f'Pack energy = {Ns * V_cell * Ah_cell}, for Ns = {Ns}, V_cell = {V_cell}, Ah_cell = {Ah_cell}')
                Np_min = math.ceil(E_min / (Ns*V_cell * Ah_cell)) # Rounding up
                print(f'Minimum Energy = {E_min}, subsequent parallel = {Np_min}')
                Np_max = math.floor(E_max / (Ns*V_cell * Ah_cell)) # Rounding down
                print(f'Maximum Energy = {E_max}, subsequent parallel = {Np_max}')
                Np_options = np.arange(Np_min, Np_max + 1, step=1)

                for Np in Np_options:
                    config = (Ns, Np, seg)
                    potential_configs.append(config)
            else:
                pass # for series combinations where it can't be divided into the given number of segments

    return potential_configs


options = calc('P50B', 350, 20, 21, 2)
print(options)
