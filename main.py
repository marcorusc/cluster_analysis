import utils
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import seaborn as sb
import sys

github = "./data/"


for file in os.listdir(github):
    if file.endswith('.csv'):
        value = file[:-8]
        file_csv = github + file
        data = pd.read_csv(file_csv)
        data = data.rename(columns={"Unnamed: 0" : "time(min)"})
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

        test = data.melt(id_vars=["time(min)"])
        sb.set_style("whitegrid")
        sb.set_palette("Oranges_r")
        g = sb.FacetGrid(test, col="variable", height=8, aspect=1.7)

        g.map(sb.lineplot, "time(min)", "value", alpha=.7)
        g.add_legend()

        title = file + value + ".png"

        g.savefig(title)