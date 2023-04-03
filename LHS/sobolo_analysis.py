import subprocess
import os
import numpy as np
import pandas as pd
from SALib.sample import saltelli
from SALib.analyze import sobol
import xml.etree.ElementTree as ET

# Define the parameter ranges
problem = {
    'num_vars': 7,
    'names': ['cell_ecm_repulsion', 'cell_junctions_attach_threshold',
              'cell_junctions_detach_threshold', 'contact_cell_cell_threshold',
              'contact_cell_ECM_threshold', 'migration_bias', 'migration_speed'],
    'bounds': [[0, 50], [0, 1], [0, 5], [0, 1], [0, 1], [0, 1], [0, 2]]
}

# Generate the input samples
param_values = saltelli.sample(problem, 1000)

# Define the input file for the simulation
input_file = './config/PhysiCell_settings_2D.xml'

# Define the command to run the simulation
simulation_cmd = './Invasion_model ./config/PhysiCell_settings_2D.xml'

# Define the output file for the simulation
output_file = 'data.csv'


tree = ET.parse(input_file)
root = tree.getroot()

for child in root:
    if child.tag == 'user_parameters':
        new_root = child

# Run the simulation for each set of input parameters
for i in range(len(param_values)):
    # Update the input file with the new parameters
    a = new_root.find('cell_ecm_repulsion')
    a.text = str(param_values[i][0])
    print(a.text)
    a = new_root.find('cell_junctions_attach_threshold')
    a.text = str(param_values[i][1])
    print(a.text)
    a = new_root.find('cell_junctions_detach_threshold')
    a.text = str(param_values[i][2])
    print(a.text)
    a = new_root.find('contact_cell_cell_threshold')
    a.text = str(param_values[i][3])
    print(a.text)
    a = new_root.find('contact_cell_ECM_threshold')
    a.text = str(param_values[i][4])
    print(a.text)
    a = new_root.find('migration_bias')
    a.text = str(param_values[i][5])
    print(a.text)
    a = new_root.find('migration_speed')
    a.text = str(param_values[i][6])
    print(a.text)
    tree.write(input_file)
    # Run the simulation
    subprocess.run(simulation_cmd, shell=True)
    os.system("python collect_data.py")
    # Save the output to a file
    if i == 0:
        df = pd.read_csv(output_file, header=None, names=['single', 'cluster', 'total_cell_in_cluster', 'cell_ratio'])
        data = np.zeros((len(param_values), len(df.columns)))
        print(data)
    else:
        df = pd.read_csv(output_file, header=None)
    data[i, :] = df.mean(axis=0)
    print(df)
    os.remove('data.csv')
# Perform the sensitivity analysis
Si = sobol.analyze(problem, data, print_to_console=True)