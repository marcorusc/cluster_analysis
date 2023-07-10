import xml.etree.ElementTree as ET
import numpy as np
import subprocess
import sys

# Define the path to your XML input file
input_file_path = sys.argv[1]
replicates = 20
# Define the path to the LHS sampling file we generated earlier
lhs_file_path = "lhs_sampling.csv"

# Load the LHS sampling file
lhs_data = np.loadtxt(lhs_file_path, delimiter=",", skiprows=1)

# Load the input XML file and get the root element
tree = ET.parse(input_file_path)
root = tree.getroot()

# Define a dictionary mapping parameter names to the indices of the corresponding columns in the LHS data
param_names = {"cell_ecm_repulsion": 0, "contact_cell_ECM_threshold": 1, "contact_cell_cell_threshold": 2, "cell_junctions_attach_threshold": 3,
               "cell_junctions_detach_threshold": 4, "migration_bias": 5, "migration_speed": 6, "persistence":7}

# Loop over each iteration in the LHS data
for i, lhs_iteration in enumerate(lhs_data):

    # Loop over each parameter and update its value in the XML file
    for param_name, lhs_col_index in param_names.items():
        param_value = lhs_iteration[lhs_col_index]
        param_xpath = f".//{param_name}/text()"
        param_element = root.find(param_xpath)
        param_element.text = str(param_value)

    # Write the updated XML to a string
    updated_xml_str = ET.tostring(root, encoding="unicode", method="xml")

    # Define the command to call your C++ software with the updated XML as input
    command = ["./Invasion_model", "./config/PhysiCell_settings_2D.xml"]
    stdin_str = updated_xml_str
    for i in range(replicates):
        # Call the C++ software using subprocess
        proc = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = proc.communicate(stdin_str.encode())

        # Check that the C++ software completed successfully
        if proc.returncode != 0:
            print(f"Error running C++ software for iteration {i}")
            print(stderr.decode())
            continue

        subprocess.run(["python", "collect_data.py"])

    subprocess.run(["python", "merge_data.py"])
    print("NEXT SET")

