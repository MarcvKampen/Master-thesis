import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('paper_celdc.csv')

df_sorted = df.sort_values('fold_enrichment', ascending=False)

top_labels = df_sorted.head(15)

plt.figure(figsize=(10, 6))
plt.barh(top_labels['label'], top_labels['fold_enrichment'], color='#1f77b4')
plt.xlabel('Fold Enrichment')
plt.ylabel('Label')
plt.title('GO cellular component, Higginbotham et al.')
plt.tight_layout()

plt.savefig('bar_chart_all_cel_func.jpg', format='jpeg')

plt.show()
