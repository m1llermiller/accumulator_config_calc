import csv
from datetime import datetime


def assign_match_score(CO_params, VD_params):

    ranking_vd = VD_params[0]
    voltage_vd = float(VD_params[1])
    ratio_vd = float(VD_params[2])

    config_CO = CO_params[0]
    voltage_co = float(CO_params[1])
    ratio_co = float(CO_params[2])

    if ratio_co <= ratio_vd:
        ratio_score = 1.0
    else:
        ratio_score = abs(ratio_co - ratio_vd) / ratio_co

    voltage_diff = abs(voltage_vd - voltage_co) / max(voltage_vd, voltage_co)
    voltage_score = 1 - voltage_diff

    match_score = ratio_score * voltage_score

    return match_score


def main():

    filepath_VD = 'UGR_cell_selection_optimisations.csv'
    filepath_CO = 'ConfigOptions_1728.csv'

    timestamp = datetime.now().strftime("%H%M")
    output_file = f'Pack_Config_Optimisation_Ratings_{timestamp}.csv'

    rankings_vd = []
    voltages_vd = []
    ratios_vd = []

    # ----- Load VD file -----
    with open(filepath_VD) as vd_file_object:

        next(vd_file_object)
        reader_vd = csv.reader(vd_file_object)

        for row in reader_vd:

            if row[0] == "":
                continue

            rankings_vd.append(row[0])
            voltages_vd.append(row[4])   # Voltage column
            ratios_vd.append(row[6])     # V/I Ratio column

    with open(output_file, mode="w", newline="") as f:

        writer = csv.writer(f)

        header = ["Config Name"] + rankings_vd
        writer.writerow(header)

        with open(filepath_CO) as co_file_object:

            next(co_file_object)
            reader_co = csv.reader(co_file_object)

            for config in reader_co:

                config_name = config[1]

                voltage_co = float(config[3])     # Nominal Pack Voltage
                current_co = float(config[7])     # Continuous Pack Current

                ratio_co = voltage_co / current_co   # Correct V/I ratio

                CO_params = [config_name, voltage_co, ratio_co]

                match_scores = []

                for x in range(len(rankings_vd)):

                    VD_params = [
                        rankings_vd[x],
                        voltages_vd[x],
                        ratios_vd[x]
                    ]

                    score = assign_match_score(CO_params, VD_params)

                    match_scores.append(score)

                match_scores.insert(0, config_name)

                writer.writerow(match_scores)

    print(f"\nOptimisation results saved to: {output_file}")


if __name__ == "__main__":
    main()