import pandas as pd
import csv
import sys
import os
import utils

if len(sys.argv) < 2:
    print("Please specify name for the output")
    sys.exit(1)

print("USING: ", sys.argv[1])

title = sys.argv[1]

output = "./output"
github = "/home/marco/Documents/PhD/github/"
physi_output = "/home/marco/Documents/PhD/github/PhysiBoSS/output/"

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

    single.append(comp_x)
    double.append(comp_y)

data = {'single': single, 'cluster': double}

df = pd.DataFrame(data)

file_csv = github + title + 'data.csv'

if os.path.exists(file_csv):
    old_data = pd.read_csv(file_csv)
    new_data = pd.concat([old_data, df], axis=1)
    new_data.to_csv(file_csv, index=False, header=True)
else:
    df.to_csv(file_csv, index=True, header=True)

