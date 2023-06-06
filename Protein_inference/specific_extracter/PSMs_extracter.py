import argparse
import csv
import os

def extract_peptides(input_files, output_file):
    all_peptide_data = []
    peptide_headers = [
        'Sequence', 'Accessions', 'nrSpectra', 'nrPSMSets', 'Missed Cleavages',
        'best scores', 'score names', 'score shorts'
    ]

    for input_file in input_files:
        with open(input_file, 'r') as csv_file:
            reader = csv.reader(csv_file)
            headers = next(reader) 
            peptide_row = next(reader)  

            # Find the index of the 'COLS_PEPTIDE' level column
            peptide_col_index = None
            for i, header in enumerate(peptide_row):
                if header == 'COLS_PEPTIDE':
                    peptide_col_index = i
                    break

            if peptide_col_index is None:
                print(f"Error: 'COLS_PEPTIDE' column not found in {input_file}. Skipping file.")
                continue

            # Filter and extract peptide data
            peptide_data = []
            for row in reader:
                if row[peptide_col_index] == 'PEPTIDE':
                    peptide_data.append(row[peptide_col_index + 1:peptide_col_index + len(peptide_headers) + 1])

            all_peptide_data.extend(peptide_data)

    with open(output_file, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(peptide_headers) 
        writer.writerows(all_peptide_data) 

    print("PSMs extracted successfully.")

def main():
    parser = argparse.ArgumentParser(description='Extract peptides from multi-level header CSV file.')
    parser.add_argument('input', type=str, help='Input CSV directory or file')
    parser.add_argument('output_file', type=str, help='Output CSV file')
    args = parser.parse_args()

    input_path = args.input
    output_file = args.output_file

    if os.path.isdir(input_path):
        input_files = [os.path.join(input_path, file) for file in os.listdir(input_path) if file.endswith('.csv')]
    elif os.path.isfile(input_path) and input_path.endswith('.csv'):
        input_files = [input_path]
    else:
        print("Error: Invalid input. Please provide a valid directory or file.")
        return

    extract_peptides(input_files, output_file)

if __name__ == '__main__':
    main()
# python fix_pia_output_PSMs.py output_step4/ output_step5/UWA_output_PSMs.csv
