import pandas as pd
import matplotlib.pyplot as plt

# List of csv files to read
csv_files = ['cv_10.csv', 'cv_20.csv', 'cv_50.csv', 'cv_100.csv', 'cv_1000.csv']

# List of colors to use for each mode
mode_colors = {'cluster': 'red', 'percentage_cluster': 'blue', 'single': 'green', 'total_cell_in_cluster': 'orange'}

# Initialize plot
fig, ax = plt.subplots()

# Loop through csv files and plot average CV for each mode
for csv_file in csv_files:
    # Read csv file
    df = pd.read_csv(csv_file)
    # Group by mode and calculate average CV
    grouped = df.groupby('mode').mean()['cv']
    # Plot average CV for each mode
    for mode, cv in grouped.items():
        ax.plot(csv_file, cv, color=mode_colors[mode], marker='o', linestyle='-')

# Set plot title and axis labels
ax.set_title('Average CV by Mode')
ax.set_xlabel('CSV File')
ax.set_ylabel('Average CV')

# Set x-axis ticks and labels
ax.set_xticks(range(len(csv_files)))
ax.set_xticklabels(csv_files)

# Set legend
ax.legend(mode_colors.keys())

# Show plot
plt.show()



