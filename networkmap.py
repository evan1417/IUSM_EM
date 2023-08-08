import pandas as pd
import plotly.graph_objects as go
import networkx as nx
import numpy as np

# Load the data CSV file
data_path = r'C:\Users\Evan Anderson\Desktop\data_with_NLP.csv'
df = pd.read_csv(data_path)

# Convert non-numeric columns to NaN
non_numeric_cols = ['acuity', 'compound']
df[non_numeric_cols] = df[non_numeric_cols].apply(pd.to_numeric, errors='coerce')

# Calculate average acuity and compound per icd.category
icd_category_stats = df.groupby('icd.category').agg({
    'acuity': 'mean',
    'compound': 'mean'
}).reset_index()

# Create the NetworkX graph
G = nx.Graph()

# Add nodes for icd.categories with their attributes
for _, row in icd_category_stats.iterrows():
    category = row['icd.category']
    G.add_node(category, **row)

# Add nodes for sites
sites = df['site'].unique()
for site in sites:
    G.add_node(site, size=5, color='green', acuity=np.nan, compound=np.nan)  # Set default acuity and compound to NaN

# Create edges between sites and icd.categories
edges = []
for _, row in df.iterrows():
    edges.append((row['site'], row['icd.category']))
G.add_edges_from(edges)

# Create positions for nodes in the plot
pos = nx.spring_layout(G, seed=42)

# Calculate positions for nodes in the plot with random initial positions
pos = nx.spring_layout(G, seed=42, pos={node: (np.random.rand(), np.random.rand()) for node in G.nodes()})

# Extract node positions, colors, and sizes for Plotly
node_x = [pos[node][0] for node in G.nodes()]
node_y = [pos[node][1] for node in G.nodes()]
node_color = ['blue' if 'icd.category' in G.nodes[node] else 'green' for node in G.nodes()]
node_size = [10 if 'icd.category' in G.nodes[node] else 5 for node in G.nodes()]

# Calculate edge widths based on the number of occurrences of icd.categories per site
edge_counts = nx.edge_betweenness_centrality(G)
edge_widths = [0.5 + 2 * edge_counts[edge] if G.nodes[edge[1]].get('icd.category') is not None else 0.5 for edge in G.edges()]

# Create the network graph using Plotly
fig = go.Figure()

# Draw edges
for edge, width in zip(G.edges(), edge_widths):
    fig.add_trace(go.Scatter(x=[pos[edge[0]][0], pos[edge[1]][0]],
                             y=[pos[edge[0]][1], pos[edge[1]][1]],
                             mode='lines',
                             line=dict(color='gray', width=width),
                             hoverinfo='none'))

# Draw nodes
node_text = []
for node in G.nodes():
    if 'icd.category' in G.nodes[node]:
        icd_categories = [edge[1] for edge in G.edges(node) if isinstance(edge[1], str)]
        node_text.append(f"{node}<br>icd.categories: {', '.join(icd_categories)}")
    else:
        icd_categories = [edge[1] for edge in G.edges(node) if isinstance(edge[1], str)]
        node_text.append(f"{node}<br>icd.categories: {', '.join(icd_categories)}" if icd_categories else node)

fig.add_trace(go.Scatter(x=node_x,
                         y=node_y,
                         mode='markers',
                         marker=dict(color=node_color,
                                     size=node_size,
                                     colorscale='Viridis',
                                     showscale=False),
                         text=list(G.nodes()),
                         hovertext=node_text,  # Use node_text to display hover information
                         hovertemplate='%{text}<extra></extra>',
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
