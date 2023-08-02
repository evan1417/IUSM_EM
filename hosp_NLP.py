import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Replace 'your_file_path' with the actual file path of the CSV file
file_path = r'C:\Users\Evan Anderson\Desktop\data_with_NLP_sorted.csv'
data = pd.read_csv(file_path)

# Calculate the average 'compound' for each descriptor listed under 'topic label'
average_compound_by_topic = data.groupby('topic label')['compound'].mean().reset_index()

# Create a graph
G = nx.Graph()

# Add nodes for the 'site' variables
sites = data['site'].unique()
for site in sites:
    G.add_node(site)

# Add nodes for the average compound of each descriptor under 'topic label'
for _, row in average_compound_by_topic.iterrows():
    topic_label = row['topic label']
    G.add_node(topic_label)

# Add edges between 'site' and average compound nodes
for _, row in data.iterrows():
    site = row['site']
    topic_label = row['topic label']
    compound = row['compound']

    G.add_edge(site, topic_label, weight=compound)

# Convert 'acuity' column to numeric type
data['acuity'] = pd.to_numeric(data['acuity'], errors='coerce')

# Create a stored dataset for 'icd.category' and 'acuity'
icd_acuity_data = data[data['acuity'] <= 3][['icd.category', 'acuity', 'topic label']]

# Add edges between 'icd.category' and average compound nodes (if acuity is <= 3)
for _, row in icd_acuity_data.iterrows():
    icd_category = row['icd.category']
    topic_label = row['topic label']
    compound = data[data['topic label'] == topic_label]['compound'].mean()

    G.add_edge(icd_category, topic_label, weight=compound, thickness='bold')

# Add edges between 'los.min', 'patient.age', and average compound nodes
for _, row in data.iterrows():
    los_min = row['los.min']
    if los_min == '*':  # Ignore non-numeric values
        continue
    los_min = float(los_min)
    patient_age = row['patient.age']
    topic_label = row['topic label']
    compound = row['compound']

    if los_min > 120:
        G.add_edge('los.min > 120', topic_label, weight=compound, thickness='bold')

# Create a figure and axis for the plot
plt.figure(figsize=(10, 8))
ax = plt.gca()

# Draw nodes and edges
pos = nx.spring_layout(G, seed=42)  # Adjust the layout algorithm as needed
nx.draw(G, pos, with_labels=True, node_size=2000, node_color='skyblue', font_size=8, font_weight='bold', font_color='black', ax=ax)
nx.draw_networkx_edges(G, pos, width=[1.5 if 'thickness' in G.edges[edge] else 1.0 for edge in G.edges()], ax=ax)

# Add edge labels with compound values
edge_labels = {(u, v): f"{G[u][v]['weight']:.2f}" for u, v in G.edges() if 'weight' in G[u][v]}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=6, font_color='red', ax=ax)

plt.title("Network Plot")
plt.show()
