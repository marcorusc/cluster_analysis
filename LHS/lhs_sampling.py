import pandas as pd
from SALib.sample import latin, sobol
import sys
import numpy as np

# Define the number of samples and parameters
num_samples = int(sys.argv[1])
num_params = 7

# Define the ranges for each parameter
param_ranges = {
    'cell_ecm_repulsion': [0, 75],
    'contact_cell_ECM_threshold': [0, 2],
    'contact_cell_cell_threshold': [0, 3.5],
    'cell_junctions_attach_threshold': [0, 1],
    'cell_junctions_detach_threshold': [0, 1],
    'migration_bias': [0, 1],
    'migration_speed': [0, 1]
}

problem = {
    'num_vars': 7,
    'names': list(param_ranges.keys()),
    'bounds': [[0, 75], [0, 2], [0, 3.5], [0, 1], [0, 1], [0, 1], [0, 1]]
}

# Generate the Latin hypercube samples
lhs_samples = latin.sample(problem, num_samples)

# Add the parameter names to the first row
param_names = list(param_ranges.keys())
param_names_str = ','.join(param_names)
lhs_samples = pd.DataFrame(lhs_samples, columns=param_names)
lhs_samples = pd.concat([pd.Series([param_names_str]), lhs_samples], axis=0, ignore_index=True)

# Save the Latin hypercube samples to a CSV file
lhs_samples.to_csv('lhs_samples.csv', index=False)

# Generate the Saltelli samples
saltelli_samples = sobol.sample(problem, num_samples)

# Add the parameter names to the first row
saltelli_samples = pd.DataFrame(saltelli_samples, columns=param_names)
saltelli_samples = pd.concat([pd.Series([param_names_str]), saltelli_samples], axis=0, ignore_index=True)

# Save the Saltelli samples to a CSV file
saltelli_samples.to_csv('saltelli_samples.csv', index=False)
