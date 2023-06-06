import argparse
import csv
import re
import os

def extract_protein_info(fasta_data, protein_id):
    pattern = r'\|{}[^|]*\|([^[]+)'.format(protein_id)
    match = re.search(pattern, fasta_data)
    if match:
        return match.group(1).strip()
    return None

def process_files(csv_file, fasta_file, output_file):
    with open(csv_file, 'r', newline='') as f:
        reader = csv.reader(f)
        rows = list(reader)
        header = rows[0]
        protein_id_index = header.index('Proteins')

        with open(fasta_file, 'r') as fasta:
            fasta_data = fasta.read()

        protein_info_index = len(header)
        header.append('protein_information')

        for row in rows[1:]:
            protein_id = row[protein_id_index]
            protein_info = extract_protein_info(fasta_data, protein_id)
            row.append(protein_info)

    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    print(f'Output CSV file saved as: {output_file}')

def main():
    parser = argparse.ArgumentParser(description='Protein ID matching and extraction')
    parser.add_argument('csv_file', help='Input CSV file path')
    parser.add_argument('fasta_file', help='Input FASTA file path')
    parser.add_argument('output_file', help='Output CSV file path and name')
    args = parser.parse_args()

    process_files(args.csv_file, args.fasta_file, args.output_file)
    print('Protein information extraction completed.')

if __name__ == '__main__':
    main()
