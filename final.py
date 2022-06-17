import utils
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import seaborn as sb
import sys

github = "./data/"



df = pd.DataFrame(columns=["variable", "mode", "count"])

for file in os.listdir(github):
    if file.endswith(".csv"):
        data = pd.read_csv(github + file)
        data = data.rename(columns={"Unnamed: 0": "time(min)"})
        for col in data:
            if col == "time(min)":
                continue
            elif col == "single":
                continue
            elif col == "cluster":
                continue
            elif col.startswith("single"):
                data = data.rename(columns={col: "single"})
            elif col.startswith("cluster"):
                data = data.rename(columns={col: "cluster"})
            else:
                print("error in dataframe")

        data["time(min)"] *= 10
        mode = [i for i in data]
        mode.remove(mode[0])
        elems = [i for i in data.iloc[-1]]
        elems.remove(elems[0])
        value = float(file[:-8])
        values = [value] * len(elems)
        total = [values, mode, elems]
        total = list(map(list, zip(*total)))
        df = df.append(pd.DataFrame(total, columns=df.columns), ignore_index=True)


ax = sb.boxplot(x="mode", y="count", hue='variable', data=df)
ax.figure.savefig("final_plot.png")