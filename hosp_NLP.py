import pandas as pd
import matplotlib.pyplot as plt

def process_csv(input_file):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(input_file)

    # Group data by 'site' and 'Topic Label' to count occurrences
    grouped_data = df.groupby(['site', 'Topic Label']).size().reset_index(name='Frequency')

    # Pivot the DataFrame to get 'site' as rows, 'Topic Label' as columns, and 'Frequency' as values
    pivot_table = grouped_data.pivot(index='site', columns='Topic Label', values='Frequency')
    pivot_table = pivot_table.fillna(0)  # Replace NaN with 0 if some combinations are missing

    #testing data to create a bar plot per hospital
    # Visualize the data using a bar plot
    #outputs simple linear
    plt.figure(figsize=(12, 6))
    pivot_table.plot(kind='bar', stacked=True, colormap='viridis')
    plt.xlabel('Site')
    plt.ylabel('Frequency')
    plt.title('Frequency of Topic Labels per Site')
    plt.legend(title='Topic Label')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Replace 'input_file.csv' with the path to your actual CSV file
    process_csv(r'C:\\Users\Evan Anderson\Desktop\data_with_NLP_sorted.csv')