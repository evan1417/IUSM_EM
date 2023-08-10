import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the data
data = pd.read_csv('/Users/evan/Desktop/data_with_NLP.csv')

# Pivot the data to create a heatmap using median as the aggregation function
heatmap_data = data.pivot_table(values='compound', index='site', columns='icd.category', aggfunc='median')

# Create a heatmap with adjusted colormap and formatting
plt.figure(figsize=(12, 8))
sns.heatmap(heatmap_data, cmap='RdBu_r', center=0, annot=True, fmt=".2f", linewidths=0.5, cbar_kws={'label': 'Compound Score'})
plt.title('Median Compound Scores by Site and icd.category')
plt.xlabel('icd.category')
plt.ylabel('Site')
plt.tight_layout()  # Ensures labels and ticks fit within the plot
plt.show()
