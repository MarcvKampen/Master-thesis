import argparse
import csv
from matplotlib import pyplot as plt
from matplotlib_venn import venn2

def read_csv_file(file_path, column_name):
    data = []
    with open(file_path, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            if column_name in row:
                data.append(row[column_name])
    return data

def get_protein_ids(file_path, column_name):
    protein_ids = set()  
    protein_info = read_csv_file(file_path, column_name)
    for info in protein_info:
        protein_ids.add(info)  
    return protein_ids

def count_matches(file1, file2):
    protein_ids1 = get_protein_ids(file1, 'RefSeq_ID')
    protein_ids2 = get_protein_ids(file2, 'refseq_id')

    num_matches = len(protein_ids1.intersection(protein_ids2))
    return num_matches

def print_unmatched_protein_ids(file1, file2):
    protein_ids1 = get_protein_ids(file1, 'RefSeq_ID')
    protein_ids2 = get_protein_ids(file2, 'refseq_id')

    unmatched_protein_ids = protein_ids2.difference(protein_ids1)
    if len(unmatched_protein_ids) > 0:
        print("Protein IDs in the second file without a match:")
        for protein_id in unmatched_protein_ids:
            print(protein_id)
    else:
        print("All protein IDs in the second file have a match.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Compare protein IDs in two CSV files.')
    parser.add_argument('file1', help='Path to the first input CSV file')
    parser.add_argument('file2', help='Path to the second input CSV file') #own file
    parser.add_argument('--label1', default='Higginbotham et al.', help='Label for the first circle')
    parser.add_argument('--label2', default='van Kampen et al.', help='Label for the second circle')
    args = parser.parse_args()

    protein_ids_file1 = get_protein_ids(args.file1, 'RefSeq_ID')
    protein_ids_file2 = get_protein_ids(args.file2, 'refseq_id')

    print(f'Number of protein IDs found in {args.file1}: {len(protein_ids_file1)}')
    print(f'Number of protein IDs found in {args.file2}: {len(protein_ids_file2)}')

    num_matches = count_matches(args.file1, args.file2)
    print(f'Number of matches: {num_matches}')

    color1 = '#A4D7FF'
    color2 = '#001B5E'

    venn2(subsets=(len(protein_ids_file1) - num_matches, len(protein_ids_file2) - num_matches, num_matches),
          set_labels=(args.label1, args.label2),
          set_colors=(color1, color2))

    plt.title('Unique protein overlap')
    plt.savefig('venn_diagram.jpg', format='jpeg')  # Save the Venn diagram as a JPEG image file

    print_unmatched_protein_ids(args.file1, args.file2)
