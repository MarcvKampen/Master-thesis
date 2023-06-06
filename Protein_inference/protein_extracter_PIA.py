import argparse
import csv
import os


def extract_protein_and_peptides(input_files, output_file):
    all_protein_data = []
    peptide_sequences = {}

    for input_file in input_files:
        with open(input_file, 'r') as csv_file:
            reader = csv.reader(csv_file)
            headers = next(reader) 

            protein_col_index = None
            for i, header in enumerate(headers):
                if header == 'COLS_PROTEIN':
                    protein_col_index = i
                    break

            if protein_col_index is None:
                print(f"Error: 'COLS_PROTEIN' column not found in {input_file}. Skipping file.")
                continue

            protein_headers = [
                'Proteins', 'Score', 'Coverages', 'nrPeptides', 'nrPSM',
                'nrSpectra', 'ClusterID', 'Description', 'Decoy', 'FDR q-value'
            ]

            protein_data = []
            current_protein_id = None

            for row in reader:
                if row[protein_col_index] == 'PROTEIN':
                    current_protein_id = row[protein_col_index + 1]
                    protein_data.append(row[protein_col_index + 1:protein_col_index + len(protein_headers) + 1])
                elif row[protein_col_index] == 'PEPTIDE' and current_protein_id:
                    peptide_sequence = row[protein_col_index + 1]
                    if current_protein_id in peptide_sequences:
                        peptide_sequences[current_protein_id].append(peptide_sequence)
                    else:
                        peptide_sequences[current_protein_id] = [peptide_sequence]

            all_protein_data.extend(protein_data)

    merged_sequences = merge_duplicate_protein_ids(peptide_sequences)

    with open(output_file, 'a', newline='') as csv_file:
        writer = csv.writer(csv_file)
        for protein_data in all_protein_data:
            protein_id = protein_data[0]
            peptide_sequence = merged_sequences.get(protein_id, '')
            writer.writerow([protein_id, peptide_sequence] + protein_data[1:])

    print("Proteins and peptide sequences extracted successfully.")


def extract_peptides(input_file):
    peptide_sequences = {}
    current_protein_id = None
    with open(input_file, 'r') as file:
        reader = csv.reader(file, delimiter=',')
        for row in reader:
            if row[0] == 'PROTEIN':
                current_protein_id = row[1]
            elif row[0] == 'PEPTIDE' and current_protein_id:
                peptide_sequence = row[1]
                if current_protein_id in peptide_sequences:
                    peptide_sequences[current_protein_id].append(peptide_sequence)
                else:
                    peptide_sequences[current_protein_id] = [peptide_sequence]
    return peptide_sequences


def merge_duplicate_protein_ids(peptide_sequences):
    merged_sequences = {}
    for protein_id, sequences in peptide_sequences.items():
        merged_sequences[protein_id] = ', '.join(sequences)
    return merged_sequences


def main():
    parser = argparse.ArgumentParser(description='Extract proteins and peptide sequences from multi-level header CSV file.')
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

    extract_protein_and_peptides(input_files, output_file)


if __name__ == '__main__':
    main()
