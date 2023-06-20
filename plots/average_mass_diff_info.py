import argparse
import csv
import matplotlib.pyplot as plt

def create_groups(input_file, output_file, bar_width=0.8):
    mass_diff_list = []
    sequence_list = []
    with open(input_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            mass_diff = float(row['mass_diff'])
            sequence = row['sequence']
            if abs(mass_diff) > 1:
                mass_diff_list.append(mass_diff)
                sequence_list.append(sequence)

    sorted_data = sorted(zip(mass_diff_list, sequence_list), key=lambda x: x[0])
    mass_diff_list, sequence_list = zip(*sorted_data)

    groups = []
    group = [(mass_diff_list[0], sequence_list[0])]
    for i in range(1, len(mass_diff_list)):
        if mass_diff_list[i] - group[-1][0] <= 0.1:
            group.append((mass_diff_list[i], sequence_list[i]))
        else:
            if len(group) > 150:
                groups.append(group)
            group = [(mass_diff_list[i], sequence_list[i])]

    if len(group) > 150:
        groups.append(group)

    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["group_number", "mass_diff", "average_mass_diff", "sequence"])
        for i, group in enumerate(groups, start=1):
            avg_mass_diff = sum(mass for mass, _ in group) / len(group)
            for mass_diff, sequence in group:
                writer.writerow([i, mass_diff, avg_mass_diff, sequence])

    avg_mass_diffs = [sum(mass for mass, _ in group) / len(group) for group in groups]
    frequencies = [len(group) for group in groups]

    plt.figure(figsize=(12, 6))  # Adjust the width and height as per your preference

    plt.bar(avg_mass_diffs, frequencies, width=bar_width)
    plt.xlabel("Average Mass Difference")
    plt.ylabel("Frequency")
    plt.title("Group Frequencies by Average Mass Difference")
    plt.savefig(output_file + '.jpeg')
    plt.show()

    print("Groups created and saved in", output_file)
    print("Plot saved as", output_file + '.jpeg')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Group mass differences in a .csv file.')
    parser.add_argument('input_file', help='input .csv file')
    parser.add_argument('output_file', help='output file without extension')
    parser.add_argument('--bar_width', type=float, default=0.4, help='width of the bars in the bar plot')
    args = parser.parse_args()

    create_groups(args.input_file, args.output_file, bar_width=args.bar_width)
