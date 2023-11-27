import os
import pandas as pd
import matplotlib.pyplot as plt

# Construct the file path
file_path = "C://Users/Evan Anderson/Desktop/Hospital_General_Information.csv"
data = pd.read_csv(file_path)

# Read the CSV file
data = pd.read_csv(file_path)

# Sort the data by 'Hospital_Ownership' column
sorted_data = data.sort_values(by='Hospital_Ownership')

# Tally the number of hospitals in each ownership category
ownership_counts = sorted_data['Hospital_Ownership'].value_counts()

# Plotting the bar chart
plt.figure(figsize=(10, 6))
ownership_counts.plot(kind='bar', color='skyblue')
plt.title('Number of Hospitals by Ownership Type')
plt.xlabel('Ownership Type')
plt.ylabel('Number of Hospitals')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()
