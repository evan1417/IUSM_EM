import pandas as pd
import plotly.express as px
from collections import Counter

# Load your data
#mac
#data_path = r'/Users/evan/Desktop/data_with_NLP.csv'
#windows
data_path = r'C:\Users\Evan Anderson\Desktop\data_with_NLP.csv'
df = pd.read_csv(data_path)


# Filter out rows where icd.category is empty
df_filtered = df[df['icd.category'].notnull()]

# Remove "Gen Med" from icd.category values using .loc indexer
df_filtered.loc[:, 'icd.category'] = df_filtered['icd.category'].str.replace('Gen Med', '')

# Create a dictionary to store top icd categories per site along with their counts
top_icd_category_counts = {}

for site in df_filtered['site'].unique():
    site_data = df_filtered[df_filtered['site'] == site]
    icd_category_counts = Counter(site_data['icd.category'])
    top_icd_category_counts[site] = icd_category_counts

# Create a list to store hierarchical data with ranks
hierarchical_data = []

for site, category_counts in top_icd_category_counts.items():
    top_categories = category_counts.most_common(10)
    rank = 1
    for category, count in top_categories:
        hierarchical_data.append({
            'parent': 'IU Health Hospitals',
            'site': site,
            'icd.category': f"{rank}. {category}",  # Add rank to icd.category
            'count': count,  # Add count of occurrences
        })
        rank += 1

# Create a DataFrame from hierarchical data
hierarchical_df = pd.DataFrame(hierarchical_data)

# Explode the icd.category list into separate rows
exploded_df = hierarchical_df.explode('icd.category')

# Create the treemap figure with adjusted width and height
fig = px.treemap(
    exploded_df,
    path=['parent', 'site', 'icd.category'],
    values=[1] * len(exploded_df),  # Equal value for all items
    title="Top 10 ICD Categories per Site",
    width=2000,
    height=2000,
    branchvalues='total',  # Set all boxes to have the same size
    custom_data=['icd.category', 'count'],  # Add custom data for hover
)

# Update text font size for all elements within the treemap traces
fig.update_traces(
    textfont_size=12,
    hovertemplate='<b>%{label}</b><br>ICD Category: %{customdata[0]}<br>Count: %{customdata[1]}<br>Value: %{value}'
)

# Show the plot
fig.show()
