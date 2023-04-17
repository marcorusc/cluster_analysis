import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import seaborn as sb
import sys
from scipy import stats
from sklearn.metrics import r2_score
from scipy.stats import norm

if len(sys.argv) < 2:
    print("Please specify name for the output")
    sys.exit(1)

github = "./data/" + sys.argv[1] + "/"

df = pd.DataFrame(columns=["value", "mode", "count"])

for file in os.listdir(github):
    if file.endswith(".csv"):
        data = pd.read_csv(github + file)
        data = data.rename(columns={"Unnamed: 0": "time(min)"})
        index = 0
        for col in data:
            if col == "time(min)":
                continue
            elif col == "single":
                index += 1
                continue
            elif col == "cluster":
                index += 1
                continue
            elif col == "total_cell_in_cluster":
                index += 1
                continue
            elif col == "cell_ratio":
                index += 1
                a = data.iloc[:, [index - 1]]["total_cell_in_cluster"]
                b = data.iloc[:, [index - 1, index - 3]].sum(axis=1)
                c = a / b
                data[col] = c * 100  # operating percentage instead of ratio
                data = data.rename(columns={col: "percentage_cluster"})
                continue
            elif col.startswith("single"):
                index += 1
                data = data.rename(columns={col: "single"})
            elif col.startswith("cluster"):
                index += 1
                data = data.rename(columns={col: "cluster"})
            elif col.startswith("total"):
                index += 1
                data = data.rename(columns={col: "total_cell_in_cluster"})
            elif col.startswith("cell"):
                index += 1
                a = data.iloc[:, [index - 1]]["total_cell_in_cluster"]
                b = data.iloc[:, [index - 1, index - 3]].sum(axis=1)
                c = a / b
                data[col] = c * 100  # operating percentage instead of ratio
                data = data.rename(columns={col: "percentage_cluster"})
            else:
                print("error in dataframe")

        data["time(min)"] *= 10
        mode = [i for i in
                data]  # collect all the modes (single, collectiv eetc...) from a single file. The number of modes should be as much as the run done for each value.
        mode.remove(mode[0])  # removing the first column which is the timestep in min
        elems = [i for i in data.iloc[3]]  # here I am taking the last values of the file
        elems.remove(elems[0])  # here I am collecting the count (number of cells or ratio) for each mode
        value = float(file[:-8])  # from the file name I am taking the value assigned to the parameter I am analysing
        values = [value] * len(elems)
        total = [values, mode, elems]
        total = list(map(list, zip(*total)))
        total = pd.DataFrame(total, columns=df.columns)
        df = pd.concat([df, pd.DataFrame(total, columns=df.columns)], ignore_index=True)

df_mode1 = df[df["mode"] == "single"]
df_mode2 = df[df["mode"] == "cluster"]
df_mode3 = df[df["mode"] == "total_cell_in_cluster"]
df_mode4 = df[df["mode"] == "percentage_cluster"]

df_numpy=df_mode1["count"].to_numpy(dtype ='float32')

# Fit a Gaussian distribution to the data
mu, std = stats.norm.fit(df_numpy)
print(mu, "  ", std)
# Calculate the R-squared value
x = np.linspace(df_numpy.min(), df_numpy.max(), 1100)
# Plot the data and the fitted Gaussian curve
fig, ax = plt.subplots()
# plot histogram
plt.hist(df_numpy, bins=30, density=True, alpha=0.5)

# plot PDF
xmin, xmax = plt.xlim()
x = np.linspace(xmin, xmax, 1100)
p = norm.pdf(x, mu, std)
plt.plot(x, p, 'k', linewidth=2)
y = stats.norm.pdf(x, mu, std)
r2 = r2_score(df_numpy, y)
print(r2)
# Add the R-squared value to the plot
ax.text(0.05, 0.95, f'R-squared = {r2:.3f}', transform=ax.transAxes, va='top')

plt.show()