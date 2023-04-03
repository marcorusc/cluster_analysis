import pandas as pd
import numpy as np
from SALib.analyze import sobol

# Read in the CSV file
df = pd.read_csv('results.csv')

# Separate the parameter values and output values
params = df.iloc[:, 1:8].to_numpy()
outputs = df.iloc[:, 8:].to_numpy()

# Perform Sobol analysis
num_params = params.shape[1]
problem = {'num_vars': num_params, 'names': ['param1', 'param2', 'param3', 'param4', 'param5', 'param6', 'param7'], 'bounds': [[0.1, 0.9]]*num_params}
param_indices = list(range(num_params))
S = sobol.analyze(problem, outputs, param_indices)

# Print the first-order and total sensitivity indices for each parameter
print('Sobol Analysis Results:')
for i, param in enumerate(problem['names']):
    print(f"{param}: S1={S['S1'][i]:.3f}, ST={S['ST'][i]:.3f}")

# Calculate the correlation matrix
corr_matrix = np.corrcoef(df.to_numpy().T)

# Extract the correlations between parameters and output variables
param_corr = corr_matrix[:7, 7:]
output_corr = corr_matrix[7:, 7:]

# Print the correlation coefficients for each parameter-output variable pair
print('\nParameter-Output Correlation Coefficients:')
for i, param in enumerate(['param1', 'param2', 'param3', 'param4', 'param5', 'param6', 'param7']):
    for j, output in enumerate(['single_cell', 'cluster', 'cell_in_cluster', 'ratio']):
        print(f'{param} - {output}: {param_corr[i,j]:.3f}')

# Print the correlation coefficients between output variables
print('\nOutput-Output Correlation Coefficients:')
for i, output1 in enumerate(['single_cell', 'cluster', 'cell_in_cluster', 'ratio']):
    for j, output2 in enumerate(['single_cell', 'cluster', 'cell_in_cluster', 'ratio']):
        print(f'{output1} - {output2}: {output_corr[i,j]:.3f}')
