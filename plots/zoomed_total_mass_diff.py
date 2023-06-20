import pandas as pd
import matplotlib.pyplot as plt

title = "Total observed mass differences"

df = pd.read_csv('merged_output.mod.csv')

df = df[(df['mass_diff'] >= 1) | (df['mass_diff'] <= -1)]


plt.figure(figsize=(12, 6))  # Adjust the width and height as per your preference

n, bins, patches = plt.hist(df['mass_diff'], bins=1000, range=(2, 30))
plt.xlabel('Precursor mass difference (Da)')
plt.ylabel('Frequency of PSMs')

plt.title(title)

plt.xlim(2, 30)

largest_indices = n.argsort()[-7:]

plt.xticks(range(0, 31, 2))

y_offsets = [0, 0, 0, 0, 0, -250, 0]

for index, val in enumerate(largest_indices):
    plt.text(bins[val], n[val] + y_offsets[index], str(round(bins[val], 2)), ha='center', va='bottom', fontsize=7)

plt.savefig('zoomed total mass difference2.png')
plt.show()
