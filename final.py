import utils
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import seaborn as sb
import sys

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
        elems = [i for i in data.iloc[-1]]  # here I am taking the last values of the file
        elems.remove(elems[0])  # here I am collecting the count (number of cells or ratio) for each mode
        value = float(file[:-8])  # from the file name I am taking the value assigned to the parameter I am analysing
        values = [value] * len(elems)
        total = [values, mode, elems]
        total = list(map(list, zip(*total)))
        total = pd.DataFrame(total, columns=df.columns)
        df = pd.concat([df, pd.DataFrame(total, columns=df.columns)], ignore_index=True)

# sea = sb.FacetGrid(df, col="mode", height=8, aspect=1.7, sharey=True, sharex=False, col_wrap=2)
# sb.set(font_scale = 2)
# sea.map(sb.boxplot, "value", "count")

df_mode1 = df[df["mode"] == "single"]
df_mode2 = df[df["mode"] == "cluster"]
df_mode3 = df[df["mode"] == "total_cell_in_cluster"]
df_mode4 = df[df["mode"] == "percentage_cluster"]

# Create subplots for each mode
grouped = df_mode1.groupby('value')
mean_values = grouped['count'].mean().reset_index()
std_values = grouped['count'].std().reset_index()

df_error = pd.merge(mean_values, std_values, on="value", suffixes=("_mean", "_std"))

error_values = df_error["count_std"] / np.sqrt(len(df_mode1["value"].unique()))

# Create scatter plot with linear regression line and error bars
plot = sb.lmplot(x="value", y="count_mean", data=df_error, fit_reg=True, x_estimator=np.mean, height=8.27, aspect=15.7/8.27, scatter_kws={'alpha': 0.5}, line_kws={'color': 'red'})
plot.ax.errorbar(df_error["value"], df_error["count_mean"], yerr=error_values, fmt='none', ecolor='black', capsize=3)

# Set plot labels
plt.xlabel("Value")
plt.ylabel("Count")
a = df_mode1['value'].unique()
b= sorted(a)
plot.ax.set_xticks(b, b)
plot.set_xticklabels(plot.ax.get_xticklabels(), rotation=75, horizontalalignment='right')
plot.fig.suptitle("Single", fontsize=12)


# # Plot linear regression for mode 2 with boxplot
grouped = df_mode2.groupby('value')
mean_values = grouped['count'].mean().reset_index()
std_values = grouped['count'].std().reset_index()

df_error = pd.merge(mean_values, std_values, on="value", suffixes=("_mean", "_std"))

error_values = df_error["count_std"] / np.sqrt(len(df_mode2["value"].unique()))

# Create scatter plot with linear regression line and error bars
plot = sb.lmplot(x="value", y="count_mean", data=df_error, fit_reg=True, x_estimator=np.mean, height=8.27, aspect=15.7/8.27, scatter_kws={'alpha': 0.5}, line_kws={'color': 'red'})
plot.ax.errorbar(df_error["value"], df_error["count_mean"], yerr=error_values, fmt='none', ecolor='black', capsize=3)

# Set plot labels
plt.xlabel("Value")
plt.ylabel("Count")
a = df_mode2['value'].unique()
b= sorted(a)
plot.ax.set_xticks(b, b)
plot.set_xticklabels(plot.ax.get_xticklabels(), rotation=75, horizontalalignment='right')
plot.fig.suptitle("Cluster", fontsize=12)


#
# # Plot linear regression for mode 3 with boxplot
grouped = df_mode3.groupby('value')
mean_values = grouped['count'].mean().reset_index()
std_values = grouped['count'].std().reset_index()

df_error = pd.merge(mean_values, std_values, on="value", suffixes=("_mean", "_std"))

error_values = df_error["count_std"] / np.sqrt(len(df_mode3["value"].unique()))

# Create scatter plot with linear regression line and error bars
plot = sb.lmplot(x="value", y="count_mean", data=df_error, fit_reg=True, x_estimator=np.mean, height=8.27, aspect=15.7/8.27, scatter_kws={'alpha': 0.5}, line_kws={'color': 'red'})
plot.ax.errorbar(df_error["value"], df_error["count_mean"], yerr=error_values, fmt='none', ecolor='black', capsize=3)

# Set plot labels
plt.xlabel("Value")
plt.ylabel("Count")
a = df_mode3['value'].unique()
b= sorted(a)
plot.ax.set_xticks(b, b)
plot.set_xticklabels(plot.ax.get_xticklabels(), rotation=75, horizontalalignment='right')
plot.fig.suptitle("total_cell_in_cluster", fontsize=12)


#
# # Plot linear regression for mode 4 with boxplot
grouped = df_mode4.groupby('value')
mean_values = grouped['count'].mean().reset_index()
std_values = grouped['count'].std().reset_index()

df_error = pd.merge(mean_values, std_values, on="value", suffixes=("_mean", "_std"))

error_values = df_error["count_std"] / np.sqrt(len(df_mode4["value"].unique()))

# Create scatter plot with linear regression line and error bars
plot = sb.lmplot(x="value", y="count_mean", data=df_error, fit_reg=True, x_estimator=np.mean, height=8.27, aspect=15.7/8.27, scatter_kws={'alpha': 0.5}, line_kws={'color': 'red'})
plot.ax.errorbar(df_error["value"], df_error["count_mean"], yerr=error_values, fmt='none', ecolor='black', capsize=3)

# Set plot labels
plt.xlabel("Value")
plt.ylabel("Count")
a = df_mode4['value'].unique()
b= sorted(a)
plot.ax.set_xticks(b, b)
plot.set_xticklabels(plot.ax.get_xticklabels(), rotation=75, horizontalalignment='right')
plot.fig.suptitle("percentage_cluster", fontsize=12)
#plt.tight_layout()
plt.show()