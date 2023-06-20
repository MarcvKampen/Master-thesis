import argparse
import csv
import matplotlib.pyplot as plt
import numpy as np

def analyze_data(csv_file):
    reader = csv.DictReader(csv_file)
    study_groups = {
        "Control": {"count": 0, "modules": {}, "mass_diffs": []},
        "Asymptomatic AD": {"count": 0, "modules": {}, "mass_diffs": []},
        "Symptomatic AD": {"count": 0, "modules": {}, "mass_diffs": []}
    }
    for row in reader:
        mass_diff = float(row["mass_diff"])
        study_group = row["study_group"]
        module = row.get("Module_Assignment_Number")  # Use get() to handle missing column gracefully
        if abs(mass_diff) > 0.0:
            study_groups[study_group]["count"] += 1
        if abs(mass_diff) < -0.0:
            study_groups[study_group]["count"] += 1
        if module:
            if module not in study_groups[study_group]["modules"]:
                study_groups[study_group]["modules"][module] = 0
            study_groups[study_group]["modules"][module] += 1
        study_groups[study_group]["mass_diffs"].append(mass_diff)

    print("Number of mass differences per study group:")
    for study_group, data in study_groups.items():
        print(f"{study_group}: {data['count']}")

    plot_histograms(study_groups)


def plot_histograms(study_groups):
    fig, axs = plt.subplots(1, 3, figsize=(30, 6))
    fig.suptitle("Amount of observed mass differences per study group")


    y_min = 0
    y_max = 450

    x_min = -150  # Adjust this value to set the desired minimum x-axis value
    x_max = 150   # Adjust this value to set the desired maximum x-axis value

    for i, (study_group, data) in enumerate(study_groups.items()):
        filtered_mass_diffs = [mass_diff for mass_diff in data["mass_diffs"] if abs(mass_diff) > 0.5]
        frequencies, bins, _ = axs[i].hist(filtered_mass_diffs, bins=1000)
        axs[i].set_title(study_group)
        axs[i].set_xlabel("Precursor mass differences (Da)")
        axs[i].set_ylabel("Frequency of PSMs")
        axs[i].set_ylim([y_min, y_max])  
        axs[i].set_xlim([x_min, x_max])

        for j, freq in enumerate(frequencies):
            if freq > 600:
                axs[i].patches[j].set_height(0)

    try:
        plt.savefig('mass_diff_per_group.png')
    except Exception as e:
        print(f"Error saving file: {e}")
    plt.show()

def compare_study_groups(study_groups):
    plot_histograms(study_groups)

    for study_group1 in study_groups:
        for study_group2 in study_groups:
            if study_group1 != study_group2:
                mass_diffs_group1 = study_groups[study_group1]["mass_diffs"]
                mass_diffs_group2 = study_groups[study_group2]["mass_diffs"]

                plot_histograms_comparison(mass_diffs_group1, mass_diffs_group2, study_group1, study_group2)

def plot_histograms_comparison(mass_diffs_group1, mass_diffs_group2, label1, label2):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(mass_diffs_group1, bins=1000, alpha=0.5, label=label1)
    ax.hist(mass_diffs_group2, bins=1000, alpha=0.5, label=label2)
    ax.set_xlabel("Mass differences (> 0.3 & < -0.3)")
    ax.set_ylabel("Frequency")
    ax.legend()
    plt.savefig(f"{label1}_vs_{label2}.png")
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_file", type=argparse.FileType("r"))
    args = parser.parse_args()
    study_groups = analyze_data(args.csv_file)
    compare_study_groups(study_groups)

