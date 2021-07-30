# This script visualizes which data points are present or not.
from covidmonte import *
import os
import seaborn as sns
import matplotlib.pyplot as plt

base_path = "data/plots/exploration"

df = get_retrospective_data()

isna = df.isna().transpose()

with Plotter(os.path.join(base_path, "sparsity.png"), figsize=(80,50)) as ax:    
    sns.heatmap(isna, ax=ax)
    ax.set_title("Which data points are present?", fontsize=60)
    ax.set_xlabel("Patient #", fontsize=60)


sns.clustermap(isna)
plt.savefig(os.path.join(base_path, "sparsity_clustered.png"))
