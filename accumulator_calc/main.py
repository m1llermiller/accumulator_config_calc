import numpy as np
import pandas as pd
import math
import csv
from datetime import datetime

# Load cell selection table
filepath = '21700_cell_options.csv'
df_raw = pd.read_csv(filepath, sep=",", index_col=0)
df_cells = df_raw.T
cell_dict = df_cells.to_dict(orient="index")

# Setup output file for calculated pack properties
timestamp = datetime.now().strftime("%H%M")  # Unique identifier for generated combinations
output_file = f'ConfigOptions_{timestamp}.csv'
output_header = [
    "Cell Name",
    "Configuration",
    "Pack Capacity (Ah)",
    "Nominal Pack Voltage (V)",
    "Max Pack Voltage (V)",
    "Nominal Module Voltage (V)",
    "Max Module Voltage (V)",
    "Nominal Pack Energy (kWh)",
    "Max Pack Energy (kWh)",
    "Nominal Module Energy (kWh)",
    "Max Module Energy (kWh)",
    "Nominal Power (kW)",
    "Cont Pack Current (A)",
    "Total Cell Count",
    "Cells per Module",
    "Total Cell Mass (kg)",
    "Cell Mass per Module (kg)",
    "Total Cell Volume (L)",
    "Cell Volume per Module (L)",
    "Pack DCIR (Ohm)",
    "Approximated Power Efficiency (%)",
    "Series Cells per Module (#)",
    "Parallel Cells (#)",
    "Number of Modules (#)",
]

with open(output_file, mode="w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(output_header)


class Pack_Param_Calc:
    '''
    This will take in the cell type and a viable configuration, from this will calculate all required fields to populate a table with the layout

    The easiest approach for writing to the file is to have all the pack parameters laid out in the first line of the csv and for each instance write a new row

    Pack parameters can be inspected using the getter - to eliminate illegal configurations

    '''

    def __init__(self, cell_name, num_series, num_parallel, num_modules, output_file):
        print(cell_name, num_series, num_parallel, num_modules)
        self.cell_name = cell_name
        self.num_series = num_series
        self.num_parallel = num_parallel
        self.num_modules = num_modules
        self.output_file = output_file

        self.param_calc()  # Initialises calculated variables

    def param_calc(self):
        # Calculate pack parameters from inputs
        self.cells_per_module = self.num_series // self.num_modules  # ensure value printed as integer
        self.configuration = f'{self.cells_per_module}s{self.num_parallel}p, {self.num_modules}s'
        self.Q_pack = self.num_parallel * float(cell_dict[self.cell_name]["Nominal Capacity (Ah)"])  # V
        self.nom_pack_v = self.num_series * float(cell_dict[self.cell_name]["Nominal Voltage (V)"])  # V
        self.max_pack_v = self.num_series * float(cell_dict[self.cell_name]["Maximum Voltage (V)"])  # V
        self.nom_mod_v = self.nom_pack_v / self.num_modules  # V
        self.max_mod_v = self.max_pack_v / self.num_modules  # V
        self.nom_pack_e = self.nom_pack_v * self.Q_pack / 1000  # kWh
        self.max_pack_e = self.max_pack_v * self.Q_pack / 1000  # kWh
        self.nom_mod_e = self.nom_mod_v * self.Q_pack / 1000  # kWh
        self.max_mod_e = self.max_mod_v * self.Q_pack / 1000  # kWh
        self.cont_pack_i = self.num_parallel * float(cell_dict[self.cell_name]["Continuous Discharge Current (A)"])  # A
        self.num_cells = self.num_parallel * self.num_series
        self.mod_num_cells = self.num_cells / self.num_modules
        self.cell_mass = self.num_cells * float(cell_dict[self.cell_name]["Mass (g)"]) / 1000  # kg
        self.mod_cell_mass = self.cell_mass / self.num_modules  # kg
        self.cell_volume = float(cell_dict[self.cell_name]["Volume (L)"]) * self.num_cells  # L
        self.mod_volume = self.cell_volume / self.num_modules  # L

        # Estimate the pack efficiency from the DCIR and output power capability
        cell_DCIR = float(cell_dict[self.cell_name]["Typical DCIR (mohm)"]) * 0.001  # convert to ohm
        self.pack_DCIR = (cell_DCIR * self.num_series) / self.num_parallel
        p_loss_kW = (
                                self.cont_pack_i ** 2 * self.pack_DCIR) / 1000  # I2R losses from continual current through pack resistance
        self.nom_power = self.nom_pack_v * self.cont_pack_i / 1000  # kW
        self.pack_efficiency = (self.nom_power - p_loss_kW) / self.nom_power

        ############# FIX this to package into sub_arrays which will make passing parameters between easier

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
            self.mod_cell_mass,
            self.cell_volume,
            self.mod_volume,
            self.pack_DCIR,
            self.pack_efficiency,
            self.cells_per_module,  # REDUNDANT - check that removing this doesnt break anything .
            self.num_parallel,
            self.num_modules, ]

    def return_pack_parameter(self, index):
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
        20  pack power efficiency approximation
        21  number of cells in each module
        22  number of parallel cells in pack
        23  number of cell modules
        '''
        return self.data_to_write[
            index]  # This can be used to check individual parameters externally so invalid layouts can be discarded

    def write_to_file(self):
        print(f'Writing to file: {self.data_to_write[1]}')
        with open(self.output_file, mode="a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(self.data_to_write)

    def copper_calc(self, p_target_kw):
        # BUSBAR MASS CALCULATIONS

        # p_target is the highest required power for operation - this will be assumed to be 80kW unless otherwise calculated by VD.
        I_requirement = p_target_kw * 1000 / self.nom_pack_v

        busbar_width_mm = 12  # assumption
        busbar_length_mm = 45  # assumption
        required_area_mm2 = 0.3723 * I_requirement - 15.359  # taken from curve fitting busbar ampacity chart

        # Calculate the required busbar height
        busbar_height_mm = required_area_mm2 / busbar_width_mm

        # Approximate volume of single busbar
        single_busbar_volume_mm3 = busbar_width_mm * busbar_length_mm * busbar_height_mm

        # Approximate mass of busbars
        copper_density_kg_per_mm3 = 8.96 * (10 ** -6)
        single_busbar_mass_kg = single_busbar_volume_mm3 * copper_density_kg_per_mm3

        # Required number of busbars = (series cells per module - 1) * number of modules
        number_busbars = (self.mod_num_cells - 1) * self.num_modules

        total_busbar_mass = number_busbars * single_busbar_mass_kg

        # PERIPHERAL TRACTIVE SYSTEM CONNECTION MASS CALCULATIONS

        '''
        generates a predicted mass of copper busbars for the pack configration, based on key assumptions:
        * relationship between area and ampacity is linear and follows calculated regression
        * width of busbars given to be 12mm - based on approximation that the busbars will be connected to the cell strips through M8 bolts. 

        for the volume calculations the assumptions are: 
        length of the busbars will be = 2.1x diameter of cell - so it spans both
        * cell width = 21.55mm
        '''


class FilterConfigurations:
    def __init__(self, pack_params):
        self.pack_params = pack_params  # Instance of pack param calc class which can be inspected
        self.feasible = True

    def FSUK_reg_filt(self):
        # checking against FSUK EV5.3.2
        if self.pack_params.return_pack_parameter(6) > 120: self.feasible = False  # Max segment voltage = 120V
        if self.pack_params.return_pack_parameter(
            10) > 6 / 3.6: self.feasible = False  # Max segment energy = 6MJ (1.66666kWh)
        if self.pack_params.return_pack_parameter(
            16) > 12: self.feasible = False  # Max segment mass = 12kg - this is for the full segment so total cell mass alone cant even be close to this
        # checking against FSUK EV4.1.1
        if self.pack_params.return_pack_parameter(4) > 600: self.feasible = False

    def UGR_limitations(self):
        # Unitek Bamocar D3 400V/400A inverter limits potential configuration options
        if self.pack_params.return_pack_parameter(
            4) > 400: self.feasible = False  # Inverter cannot handle input voltages > 400V.

    def return_check(self):
        return self.feasible


class GenerateCombinations


def calc(cell_name, v_target, v_tolerance, e_target_kWh, e_tolerance_kWh):
    potential_configs = []  # To be populated by (num_series, num_parallel, num_segments)

    cell = cell_dict[cell_name]
    V_cell = np.float64(cell["Nominal Voltage (V)"])
    Ah_cell = np.float64(cell["Nominal Capacity (Ah)"])

    # Range of acceptable pack voltages
    V_max = v_target + v_tolerance
    V_min = v_target - v_tolerance

    Ns_min = math.ceil(V_min / V_cell)
    Ns_max = math.floor(V_max / V_cell)

    # Range of acceptable series cell configurations
    Ns_options = np.arange(Ns_min, Ns_max + 1, step=1)

    # only designing for packs with between 4 and 7 segments
    segment_options = [4, 5, 6, 7]

    # Keep only the series combinations that permit division into equal cell segments
    Ns_options = [Ns for Ns in Ns_options if any(Ns % seg == 0 for seg in segment_options)]

    # Finding the subsequent required parallel cells to build to the desired capacity

    # Range of acceptable pack energies
    E_max = (e_target_kWh + e_tolerance_kWh) * 1000  # Wh
    E_min = (e_target_kWh - e_tolerance_kWh) * 1000  # Wh

    # to generate the parallel cell combinations
    for Ns in Ns_options:
        for seg in segment_options:
            if Ns % seg == 0:
                Np_min = math.ceil(E_min / (Ns * V_cell * Ah_cell))
                Np_max = math.floor(E_max / (Ns * V_cell * Ah_cell))
                Np_options = np.arange(Np_min, Np_max + 1, step=1)

                for Np in Np_options:
                    config = (cell_name, Ns, Np, seg)
                    potential_configs.append(config)
            else:
                pass  # for series combinations where it can't be divided into the given number of segments

    return potential_configs


def main():
    main_menu_text = f'---- Pack Configuration Generator ----\n[1]\tAdd accumulator config options\n[2]\tSave and exit\n>>>\t'
    while True:
        selection = int(input(main_menu_text))
        if selection == 1:
            print(f'Cell choices available: ')
            print(", ".join(cell_dict.keys()))
            # This should print the cells that have been imported
            cell_choice = input('Cell choice: ')
            v_target = float(input('Desired nominal pack voltage (V):\t'))
            v_tolerance = float(input('Permissible deviation from target pack voltage (V):\t'))
            p_target = float(input('Desired pack energy (MJ):\t')) / 3.6  # Further calculations done in terms of kWh
            p_tolerance = float(input('Permissible deviation from target pack energy (MJ):\t')) / 3.6

            config_options = calc(cell_choice, v_target, v_tolerance, p_target, p_tolerance)
            for potential_config in config_options:
                paramCalc = Pack_Param_Calc(potential_config[0], potential_config[1], potential_config[2],
                                            potential_config[3], output_file)
                filter = FilterConfigurations(paramCalc)
                filter.FSUK_reg_filt()
                filter.UGR_limitations()
                if filter.return_check() == True:
                    paramCalc.write_to_file()
                else:
                    pass

        elif selection == 2:
            break
        else:
            pass


if __name__ == "__main__":
    main()

