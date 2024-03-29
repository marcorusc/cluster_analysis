import pandas as pd
import csv
import sys
import os
import utils

if len(sys.argv) < 2:
    print("Please specify name for the output")
    sys.exit(1)

print("USING: ", sys.argv[1])

folder = sys.argv[1]

home = os.path.expanduser('~')

data_folder = home + "/data/cluster_analysis/LHS/" + folder + "/"
physi_output = home + "/PhysiBoSS/output_" + folder + "/"

list_of_file = []
list_of_svg = []

for file in os.listdir(physi_output):
    if file.startswith("final_net"):
        # print(file)
        list_of_file.append(file)
    elif file.startswith("snapshot"):
        list_of_svg.append(file)

list_of_file.sort()
list_of_file.remove(list_of_file[0])
list_of_svg.sort()

single = []
double = []
ratio = []
cell_in_cluster = []

for file in list_of_file:
    path = physi_output + file
    net_df = pd.read_csv(path)
    utils.split_col(net_df)

    I = utils.create_graph(net_df, ' neighID')
    # H = create_graph(net_df, ' neighID45')
    # L = create_graph(net_df, ' neighID90')
    # F = create_graph(net_df, ' neighID180')
    comp_x = utils.count_component(I)[0]
    comp_y = utils.count_component(I)[1]
    comp_z = utils.count_cell_in_cluster(I)[0]
    comp_w = utils.count_cell_in_cluster(I)[1]
    single.append(comp_x)
    double.append(comp_y)
    ratio.append(comp_z)
    cell_in_cluster.append(comp_w)

data = {'single': single, 'cluster': double, 'total_cell_in_cluster': cell_in_cluster, 'cell_ratio': ratio}

df = pd.DataFrame(data)
df = df.iloc[[-1]]
file_csv = data_folder + 'data.csv'

if os.path.exists(file_csv):
    old_data = pd.read_csv(file_csv)
    new_data = pd.concat([old_data, df], axis=0, ignore_index=True)
    new_data.to_csv(file_csv, index=False, header=True)
else:
    df.to_csv(file_csv, index=False, header=True)
