import argparse
import csv
import requests

def convert_uniprot_to_refseq(uniprot_id):
    url = f"https://www.uniprot.org/uniprot/{uniprot_id}.txt"
    response = requests.get(url)
    if response.status_code == 200:
        lines = response.text.split("\n")
        for line in lines:
            if line.startswith("DR   RefSeq"):
                fields = line.split(";")
                for field in fields:
                    if field.startswith(" NP_"):
                        refseq_id = field.strip().split()[0]
                        return refseq_id
    return None

def process_protein_ids(input_file):
    rows = []

    with open(input_file, 'r') as file:
        reader = csv.DictReader(file)
        fieldnames = reader.fieldnames + ['refseq_id']
        for row in reader:
            uniprot_id = row['uniprot_id']
            refseq_id = convert_uniprot_to_refseq(uniprot_id)
            if refseq_id:
                row['refseq_id'] = refseq_id
            else:
                row['refseq_id'] = 'Not found'
            rows.append(row)

    with open(input_file, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

def main():
    parser = argparse.ArgumentParser(description='Convert UniProt IDs to RefSeq IDs')
    parser.add_argument('input_file', help='Path to the input CSV file containing protein IDs') # do not give a output file, it just add an extra column
    args = parser.parse_args()

    process_protein_ids(args.input_file)

if __name__ == '__main__':
    main()
