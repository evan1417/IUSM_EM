import pandas as pd
import plotly.graph_objects as go
import networkx as nx
import numpy as np

# Load the data from CSV file
data_path = r'C:\Users\Evan Anderson\Desktop\data_with_NLP_sorted.csv'
df = pd.read_csv(data_path)

# Convert non-numeric columns to NaN
non_numeric_cols = ['acuity', 'compound']
df[non_numeric_cols] = df[non_numeric_cols].apply(pd.to_numeric, errors='coerce')

# Calculate average acuity and compound per icd.category
icd_category_stats = df.groupby('icd.category').agg({
    'acuity': 'mean',
    'compound': 'mean'
}).reset_index()

# Create a dictionary to store icd.category statistics
icd_stats_dict = {}
for _, row in icd_category_stats.iterrows():
    category = row['icd.category']
    acuity = row['acuity']
    compound = row['compound']
    icd_stats_dict[category] = {'acuity': acuity, 'compound': compound}

# Create the NetworkX graph
G = nx.Graph()

# Add nodes for icd.categories with their attributes
for category, stats in icd_stats_dict.items():
    size = abs(stats['acuity'] - icd_category_stats['acuity'].min()) + 1
    color = 'red' if stats['compound'] < 0 else 'blue'
    G.add_node(category, size=size, color=color, **stats)

# Add nodes for sites
sites = df['site'].unique()
for site in sites:
    G.add_node(site, size=5, color='green', acuity=np.nan, compound=np.nan)  # Set default acuity and compound to NaN

# Create edges between sites and icd.categories
for _, row in df.iterrows():
    G.add_edge(row['site'], row['icd.category'])

# Create positions for nodes in the plot
pos = nx.spring_layout(G, seed=42)

# Extract node positions, colors, and sizes for Plotly
node_x = [pos[node][0] for node in G.nodes()]
node_y = [pos[node][1] for node in G.nodes()]
node_color = [G.nodes[node].get('color', 'green') for node in G.nodes()]  # Use 'green' as default color for sites
node_size = [G.nodes[node].get('size', 5) for node in G.nodes()]  # Use 5 as default size for sites

# Create the network graph using Plotly
fig = go.Figure()

# Draw edges
for edge in G.edges():
    fig.add_trace(go.Scatter(x=[pos[edge[0]][0], pos[edge[1]][0]],
                             y=[pos[edge[0]][1], pos[edge[1]][1]],
                             mode='lines',
                             line=dict(color='gray', width=0.5),
                             hoverinfo='none'))

# Draw nodes
fig.add_trace(go.Scatter(x=node_x,
                         y=node_y,
                         mode='markers',
                         marker=dict(color=node_color,
                                     size=node_size,
                                     colorscale='Viridis',
                                     showscale=False),
                         text=list(G.nodes()),
                         hovertemplate='icd.category: %{text}<br>Acuity: %{customdata[0]:.2f}<br>Compound: %{customdata[1]:.2f}<extra></extra>',
                         customdata=[[G.nodes[node].get('acuity', np.nan), G.nodes[node].get('compound', np.nan)] for node in G.nodes()],
                         hoverinfo='text'))

# Add labels for icd.categories
icd_category_labels = [node for node in G.nodes() if isinstance(node, str)]
label_x = [pos[node][0] for node in icd_category_labels]
label_y = [pos[node][1] for node in icd_category_labels]

fig.update_layout(
    title='Network Graph',
    showlegend=False,
    hovermode='closest',
    annotations=[
        go.layout.Annotation(
            x=label_x[i],
            y=label_y[i],
            text=icd_category_labels[i],
            showarrow=False,
            font=dict(size=9)
        ) for i in range(len(icd_category_labels))
    ]
)

# Show the graph
fig.show()
