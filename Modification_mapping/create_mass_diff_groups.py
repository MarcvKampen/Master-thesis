import pandas as pd

df = pd.read_csv('UWA_all_group.csv')
df = df[['study_group', 'mass_diff']]
df = df[(df['mass_diff'] >= 2) | (df['mass_diff'] <= -2)]
grouped_mass_diffs = {}


for _, row in df.iterrows():
    study_group = row['study_group']
    mass_diff = row['mass_diff']
    if study_group not in grouped_mass_diffs:
        grouped_mass_diffs[study_group] = []
    grouped = False
    for group in grouped_mass_diffs[study_group]:
        if abs(mass_diff - group[0]) <= 0.005:
            group.append(mass_diff)
            grouped = True
            break
    if not grouped:
        grouped_mass_diffs[study_group].append([mass_diff])

sorted_groups = {k: sorted(v, key=len, reverse=True) for k, v in grouped_mass_diffs.items()}
sorted_groups = {k: v[:10] for k, v in sorted_groups.items()}  # Keep only the 10 largest groups

mean_mass_diffs = {k: [(group, sum(group) / len(group), len(group)) for group in v] for k, v in sorted_groups.items()}

output_data = []
for study_group, groups in mean_mass_diffs.items():
    for group, mean_mass_diff, num_members in groups:
        output_data.append([study_group, mean_mass_diff, num_members])

output_df = pd.DataFrame(output_data, columns=['study_group', 'mean_mass_diff', 'num_members'])
output_df.to_csv('output.csv', index=False)
