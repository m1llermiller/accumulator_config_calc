import numpy as np
import pandas as pd
import math
import csv
from datetime import datetime
'''
Objective for program - take viable pack configuration list and compare against the VD perfomance optimisations 
parameters list - find a way to quantify the match and assign a score (for how well they match)

output list of pack config names and the score for how it matches
> find a way to sort this - whatever is at the top should be the most optimised

parameters to compare from the two files:
VD RANKINGS:
    >   ranking
    >   V
    >   V/I ratio (calculated pack must (exceed/be lower than) the VD ranking)
    
ConfigOptions
    >   configuration name
    >   V_pack_nom
    >   V/I ratio

'''
def assign_match_score(CO_params, VD_params):
    ranking_vd, voltage_vd, ratio_vd = VD_params[0], VD_params[1], VD_params[2]
    config_CO, voltage_co, ratio_co = CO_params[0], CO_params[1], CO_params[2]

    if ratio_co <= ratio_vd:
        ratio_score = 1
    else:
        ratio_score = (ratio_vd - ratio_co) / ratio_vd # further off the config option is, the worse the score

    # higher score = better match in voltage
    voltage_diff = np.abs(voltage_vd-voltage_vd)/voltage_vd # fractional difference between voltage values
    voltage_score = 1-voltage_diff
    match_score = ratio_score * voltage_score # approximation method - higher score >> better match

    return match_score


'''    # Opens both files, creates a new table which has the top 10 optimised config options as the header
    # For every row (config) in config options, the V/I / V is compared, will return a 'FIT' score
    # FIT score > BEST = 1 (if V/I(config) < V/I(VD) ), otherwise is a decimal corresponding to how far off it is
    # goes across the columns and calculates FIT score for a given config for top 10 optimised layouts
    # goes to next config and repeats
    # returned array can help to narrow down config options
'''

def main():
    # Load cell selection table
    filepath_VD = 'UGR_cell_selection_optimisations.csv'
    filepath_CO = 'ConfigOptions_1130.csv'

    df_init = pd.read_csv(filepath_CO, sep=",", index_col=0)
    df_ConfigOptions = df_init.T
    ConfigOptions = df_ConfigOptions.to_dict(orient="index")

    df_init = pd.read_csv(filepath_CO, sep=",", index_col=0)
    df_Optimisations = df_init.T
    VDOptimised = df_Optimisations.to_dict(orient="index")

    # Setup output file for performance comparison
    timestamp = datetime.now().strftime("%H%M")  # Unique identifier for generated combinations
    output_file = f'Pack_Config_Optimisation_Ratings_{timestamp}.csv'
    output_header = ['', '']  # The top rankings

    # Loading data from dataframes
    config_CO = ConfigOptions['Configuration']
    voltage_co = ConfigOptions['Nominal Pack Voltage (V)']
    ratio_co = ConfigOptions['V/I']

    ranking_vd = VDOptimised['Ranking']
    voltage_vd = VDOptimised['Voltage']
    ratio_vd = VDOptimised['V/I Ratio']

    VD_params = [ranking_vd, voltage_vd, ratio_vd]
    CO_params = [config_CO, voltage_co, ratio_co]

    with open(output_file, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(output_header)



# needs to be some sort of inside and outside loop.