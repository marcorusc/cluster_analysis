import pandas as pd
import sys

# Set the number of output files to generate
num_files = int(sys.argv[1])

# Read in the input CSV file
df = pd.read_csv('saltelli_samples.csv')

# Calculate the number of rows in each output file
rows_per_file = int(len(df) / num_files)

# Loop over the number of output files to generate
for i in range(num_files):
    # Calculate the start and end indices for the current output file
    start_idx = i * rows_per_file
    end_idx = (i + 1) * rows_per_file

    # If this is the last file, include any remaining rows
    if i == num_files - 1:
        end_idx = len(df)

    # Extract the rows for the current output file
    rows = df.iloc[start_idx:end_idx]

    # Write the rows to a new CSV file
    filename = f'saltelli_samples_{i}.csv'
    rows.to_csv(filename, index=False)
