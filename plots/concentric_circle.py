import argparse
import csv
import math
import matplotlib.pyplot as plt

def main():
    parser = argparse.ArgumentParser(description='Concentric circle diagram')
    parser.add_argument('csv_file', help='Input CSV file path')
    parser.add_argument('output_file', help='Output JPEG file path')
    args = parser.parse_args()

    proteins = 0
    peptides = 0
    psms = 0

    with open(args.csv_file, 'r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            proteins += 1
            peptides += int(row['nrPeptides'])
            psms += int(row['nrPSM'])

    print(f'Proteins: {proteins}')
    print(f'Peptides: {peptides}')
    print(f'PSMs: {psms}')

    generate_concentric_circles(proteins, peptides, psms, args.output_file)

def generate_concentric_circles(proteins, peptides, psms, output_file):
    total_counts = psms + peptides + proteins

    scaling_factor = 0.5  # Adjust this factor to control the size of the circles
    psm_radius = scaling_factor * math.sqrt(psms / total_counts)
    peptide_radius = scaling_factor * math.sqrt(peptides / total_counts)
    protein_radius = scaling_factor * math.sqrt(proteins / total_counts)

    fig, ax = plt.subplots(figsize=(8, 8))

    psm_bottom = 0
    peptide_bottom = 0
    protein_bottom = 0

    circle1 = plt.Circle((0.5, psm_bottom + psm_radius), psm_radius, color='#A4D7FF', alpha=0.2)
    circle2 = plt.Circle((0.5, peptide_bottom + peptide_radius), peptide_radius, color='#0096FF', alpha=0.2)
    circle3 = plt.Circle((0.5, protein_bottom + protein_radius), protein_radius, color='#001B5E', alpha=0.2)

    ax.add_artist(circle1)
    ax.add_artist(circle2)
    ax.add_artist(circle3)

    # Set aspect ratio to be equal
    ax.set_aspect('equal')

    # Set plot limits
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    # Remove ticks and labels
    ax.set_xticks([])
    ax.set_yticks([])

    legend_labels = ['PSMs', 'Peptides', 'Proteins']
    legend_text = [f'{label}: {count}' for label, count in zip(legend_labels, [psms, peptides, proteins])]
    ax.legend(legend_text, loc='upper right', fontsize=12)

    plt.title('Protein Interference')
    plt.savefig(output_file, format='jpeg')
    plt.close()

if __name__ == '__main__':
    main()

