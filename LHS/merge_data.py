import pandas as pd
import os
# Read in the CSV file
df = pd.read_csv('data.csv')

# Calculate the column-wise averages
averages = df.mean()

# Create a new DataFrame with the averages
averages_df = pd.DataFrame(averages).T
output_csv = 'output.csv'
# Write the averages DataFrame to a new CSV file
averages_df.to_csv('averages.csv', index=False)

if os.path.exists(output_csv):
    old_data = pd.read_csv(output_csv)
    new_data = pd.concat([old_data, averages_df], axis=0, ignore_index=True)
    new_data.to_csv(output_csv, index=False, header=True)
else:
    averages_df.to_csv(output_csv, index=False, header=True)