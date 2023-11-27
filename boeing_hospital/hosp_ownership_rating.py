import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Construct the file path
file_path = "C://Users/Evan Anderson/Desktop/Hospital_General_Information.csv"
data = pd.read_csv(file_path)

# Sort the data by 'Hospital_Ownership' column
sorted_data = data.sort_values(by='Hospital_Ownership')

# Calculate average rating per hospital ownership type
data['Hospital_overall_rating'] = pd.to_numeric(data['Hospital_overall_rating'], errors='coerce')
avg_rating = data.groupby('Hospital_Ownership')['Hospital_overall_rating'].mean().sort_values()

# Plotting the bar chart with average ratings
plt.figure(figsize=(10, 6))

for index, (ownership, rating) in enumerate(avg_rating.items()):
    plt.bar(ownership, rating)
    plt.text(index, rating + 0.05, f'{rating:.2f}', ha='center', va='bottom', fontsize=8)

# Set labels and title
plt.title('Average Rating per Hospital Ownership Type')
plt.xlabel('Ownership Type')
plt.ylabel('Average Rating')

plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()
