import pandas as pd

df = pd.read_csv('UWA_all_group.csv')

df = df[['mass_diff']]

df = df[(df['mass_diff'] >= 1.1) | (df['mass_diff'] <= -1.1)]

groups = []

for _, row in df.iterrows():
    mass_diff = row['mass_diff']
    grouped = False
    for group in groups:
        if abs(mass_diff - group[0]) <= 0.0003:
            group.append(mass_diff)
            grouped = True
            break
    if not grouped:
        groups.append([mass_diff])

sorted_groups = sorted(groups, key=len, reverse=True)[:10]  # Keep only the 10 largest groups

mean_mass_diffs = [(group, sum(group) / len(group), len(group)) for group in sorted_groups]

output_data = []
for group, mean_mass_diff, num_members in mean_mass_diffs:
    output_data.append([mean_mass_diff, num_members])


output_df = pd.DataFrame(output_data, columns=['mean_mass_diff', 'num_members'])
output_df.to_csv('output.csv', index=False)
