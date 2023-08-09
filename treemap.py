import pandas as pd
import plotly.express as px
from collections import Counter

# Load your data
data_path = r'/Users/evan/Desktop/data_with_NLP.csv'
df = pd.read_csv(data_path)

# Filter out rows where icd.category is empty
df_filtered = df[df['icd.category'].notnull()]

# Remove "Gen Med" from icd.category values using .loc indexer
df_filtered.loc[:, 'icd.category'] = df_filtered['icd.category'].str.replace('Gen Med', '')

# Initialize a dictionary to store top icd categories per site
top_icd_categories = {}

for site in df_filtered['site'].unique():
    site_data = df_filtered[df_filtered['site'] == site]
    icd_category_counts = Counter(site_data['icd.category'])
    top_categories = icd_category_counts.most_common(10)
    top_icd_categories[site] = [category for category, _ in top_categories]

# Create a list to store hierarchical data
hierarchical_data = []

for site, categories in top_icd_categories.items():
    hierarchical_data.append({
        'parent': 'IU Health Hospitals',
        'site': site,
        'icd.category': categories  # Store the list of top categories
    })

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
    width=1000,  # Adjust the width
    height=800,  # Adjust the height
    branchvalues='total',  # Set all boxes to have the same size
    custom_data=['icd.category'],  # Add custom data for hover
)

# Update text font size for all elements within the treemap traces
fig.update_traces(
    textfont_size=12,  # Set the font size for all text
    hovertemplate='<b>%{label}</b><br>ICD Category: %{customdata[0]}<br>Value: %{value}'
)

# Show the plot
fig.show()
