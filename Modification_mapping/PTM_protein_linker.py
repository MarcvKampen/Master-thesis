import argparse
import re
import csv
import os

def remove_modifications(peptide_sequence):
    modified_sequence = re.sub(r'\[.*?\]', '', peptide_sequence)
    modified_sequence = re.sub(r'\(.*?\)', '', modified_sequence)
    return modified_sequence

def extract_accessions(input_file, peptide_sequences, check_file, output_file):
    with open(input_file, 'r') as file:
        content = file.read()

    with open(check_file, 'r') as csv_file:
        reader = csv.reader(csv_file)
        protein_ids = set(row[0] for row in reader)

    output_rows = []

    for peptide_sequence, idxml_file in peptide_sequences:
        modified_sequence = remove_modifications(peptide_sequence)
        unmodified_sequence = remove_modifications(peptide_sequence)

        pattern = r'<PeptideHit.*?sequence="{}".*?protein_refs="(.*?)".*?>'.format(re.escape(modified_sequence))
        matches = re.findall(pattern, content)

        if matches:
            protein_hits = matches[0].split()
            accessions = []

            for hit in protein_hits:
                protein_hit_pattern = r'<ProteinHit id="{}" accession="(.*?)".*?>'.format(hit)
                protein_hit_match = re.search(protein_hit_pattern, content)
                if protein_hit_match:
                    accession = protein_hit_match.group(1)
                    protein_id = accession.split('|')[1]
                    if protein_id in protein_ids:
                        accessions.append(protein_id)

            if accessions:
                output_row = [unmodified_sequence] + accessions
                output_rows.append(output_row)
            else:
                output_row = [unmodified_sequence, "No protein IDs found"]
                output_rows.append(output_row)
        else:
            output_row = [unmodified_sequence, "No matches found"]
            output_rows.append(output_row)

    with open(output_file, 'a', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(output_rows)

    print("Results appended to {}".format(output_file))

def read_peptide_sequences_from_csv(csv_file):
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        header = next(reader)
        peptide_sequences = [(row[0], row[6]) for row in reader] 
    return peptide_sequences

def find_idxml_file(csv_file):
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        peptide_idxml_files = [(row['sequence'], row['file_name']) for row in reader]
    return peptide_idxml_files

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Search for specific peptide sequences in an .idxml file and extract the corresponding protein IDs.")
    parser.add_argument("check_file", help="Path to the .csv check file")
    parser.add_argument("csv_file", help="Path to the input CSV file")
    parser.add_argument("output_file", help="Path to the output CSV file")

    args = parser.parse_args()

    peptide_idxml_files = find_idxml_file(args.csv_file)
    script_directory = os.path.dirname(os.path.abspath(__file__))

    for peptide_sequence, idxml_file in peptide_idxml_files:
        input_file_path = os.path.join(script_directory, idxml_file)

        peptide_sequences = [(peptide_sequence, input_file_path)]
        extract_accessions(input_file_path, peptide_sequences, args.check_file, args.output_file)

    print("Results appended to {}".format(args.output_file))
