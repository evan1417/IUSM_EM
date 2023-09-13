import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style('ticks')

import warnings
warnings.filterwarnings('ignore')

survey_data = pd.read_csv(r'C:\Users\Evan Anderson\Desktop\data_with_NLP.csv')
survey_data.head()

def age_group(ages):

    # Convert to an int, in case the data is read in as an "object" (aka string)
    age = int(ages)

    if age < 18:
        bucket = '<18'

    # Age 18 to 29 ('range' excludes upper bound)
    if age in range(18, 30):
        bucket = '18-29'

    if age in range(30, 40):
        bucket = '30-39'

    if age in range(40, 50):
        bucket = '40-49'

    if age in range(50,60):
        bucket = '50-59'

    if age in range(60,70):
        bucket = '60-69'

    if age >= 70:
        bucket = '70+'

    return bucket

# Apply age_group function
survey_data['age_group'] = survey_data['patient_age'].apply(age_group)

# Compute counts of each group
count_data = survey_data.groupby(['age_group', 'topic_label']).size().reset_index(name='count')

# Compute average 'compound' of each group
avg_compound_data = survey_data.groupby(['age_group', 'topic_label'])['compound'].mean().reset_index()

# Merge count_data and avg_compound_data on ['age_group', 'topic_label']
merged_data = pd.merge(count_data, avg_compound_data, on=['age_group', 'topic_label'])

# Create a colormap
cmap = plt.get_cmap("coolwarm")

# Normalize the 'compound' column to range [-1,1]
norm = plt.Normalize(merged_data['compound'].min(), merged_data['compound'].max())

# Create a color dictionary based on the 'compound' value
palette = {row['topic_label']: cmap(norm(row['compound'])) for index, row in merged_data.iterrows()}

# Specify age group order
age_order = ['<18', '18-29', '30-39', '40-49', '50-59', '60-69', '70+']

# Create the bar chart
plt.figure(figsize=(14, 8))
sns.barplot(x='age_group', y='count', hue='topic_label', data=merged_data, ci=None, order=age_order, palette=palette)

plt.title('Number of occurrences of each topic_label within each age group')
plt.xlabel('Age Group')
plt.ylabel('Count')

# Add a colorbar to explain the colormap
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
plt.colorbar(sm, label='Average Compound Score')

plt.show()