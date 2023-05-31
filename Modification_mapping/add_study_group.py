import argparse
import csv

asymptomatic = ['UWA626', 'UWA596', 'UWA419', 'UWA422', 'UWA556', 'UWA558']
control = ['UWA479', 'UWA420', 'UWA506', 'UWA531', 'UWA431', 'UWA623']
symptomatic = ['UWA576', 'UWA579', 'UWA580', 'UWA612', 'UWA614', 'UWA530']

parser = argparse.ArgumentParser(description='Update PSM_ID column in a CSV file.')
parser.add_argument('input_file', type=str, help='path to the input CSV file')
parser.add_argument('output_file', type=str, help='path to the output CSV file')
args = parser.parse_args()

with open(args.input_file, newline='') as infile, open(args.output_file, 'w', newline='') as outfile:
    reader = csv.DictReader(infile)
    fieldnames = ['study_group'] + [f for f in reader.fieldnames if f != 'PSM_ID']
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()
    for row in reader:
        uwa_id = row['PSM_ID'].split('.')[0].split('_')[0]
        if uwa_id in asymptomatic:
            row['study_group'] = 'Asymptomatic AD'
        elif uwa_id in control:
            row['study_group'] = 'Control'
        elif uwa_id in symptomatic:
            row['study_group'] = 'Symptomatic AD'
        writer.writerow({k: row[k] for k in fieldnames})
