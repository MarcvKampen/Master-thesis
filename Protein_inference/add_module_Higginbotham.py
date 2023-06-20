import argparse
import csv

def extract_protein_id(string):
    protein_id = string.split('|')[-1].strip()
    return protein_id

def merge_csv_files(file1, file2, output_file):
    protein_ids = set()
    module_data = {}

    with open(file1, 'r') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)
        refseq_id_index = header.index('refseq_id')
        for row in reader:
            protein_id = extract_protein_id(row[refseq_id_index])
            protein_ids.add(protein_id)

    with open(file2, 'r') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)
        protein_id_index = header.index('Protein_Unique_ID')
        module_number_index = header.index('Module_Assignment_(Number)')
        module_color_index = header.index('Module_Assigment_(Color)')
        for row in reader:
            protein_id = extract_protein_id(row[protein_id_index])
            if protein_id in protein_ids:
                module_data[protein_id] = (row[module_number_index], row[module_color_index])

    with open(file1, 'r') as csvfile:
        reader = csv.reader(csvfile)
        with open(output_file, 'w', newline='') as outfile:
            writer = csv.writer(outfile)
            header = next(reader)
            writer.writerow(header + ['Module_Assignment_(Number)', 'Module_Assigment_(Color)'])
            refseq_id_index = header.index('refseq_id')
            for row in reader:
                protein_id = extract_protein_id(row[refseq_id_index])
                module_assignment = module_data.get(protein_id, ('', ''))
                writer.writerow(row + [module_assignment[0], module_assignment[1]])

    print(f"Output file '{output_file}' generated successfully.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Merge two CSV files based on protein ID.')
    parser.add_argument('file1', help='Path to the first CSV file')
    parser.add_argument('file2', help='Path to the second CSV file')
    parser.add_argument('-o', '--output', help='Path to the output CSV file', default='output.csv')
    args = parser.parse_args()

    merge_csv_files(args.file1, args.file2, args.output)
