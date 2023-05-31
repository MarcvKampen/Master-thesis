import argparse
import pandas as pd
import os

parser = argparse.ArgumentParser(description='Process input file for PSM analysis')
parser.add_argument('input_file', metavar='input_file', type=str,
                    help='input file to process')
parser.add_argument('output_path', metavar='output_path', type=str,
                    help='output path for the generated files')

args = parser.parse_args()

dframe = pd.read_csv(args.input_file,
                     skiprows=2,
                     names=['sequence', 'PSM_ID', 'exp_mass_to_charge', 'calc_mass_to_charge',
                            'charge', 'mass_diff', 'exp_mass', 'mass_tol', 'mass_tol_pos',
                            'mass_tol_neg', 'file_name', 'mod','mod_mass'])

filtered_df = dframe[(dframe['mod'].notnull()) & (dframe['mod'] != "No direct match found in Unimod")]

psm_mod_list = filtered_df[['sequence', 'PSM_ID', 'exp_mass_to_charge', 'calc_mass_to_charge',
                            'charge', 'mass_diff', 'exp_mass', 'mass_tol', 'mass_tol_pos',
                            'mass_tol_neg', 'file_name', 'mod','mod_mass']].values.tolist()
psm_mod_list_df = pd.DataFrame(psm_mod_list, columns=['sequence', 'PSM_ID', 'exp_mass_to_charge', 'calc_mass_to_charge',
                            'charge', 'mass_diff', 'exp_mass', 'mass_tol', 'mass_tol_pos',
                            'mass_tol_neg', 'file_name', 'mod','mod_mass'])

output_file = os.path.join(args.output_path, os.path.basename(args.input_file.replace('.csv', '_only_list.csv')))

psm_mod_list_df.to_csv(output_file, index=False)
