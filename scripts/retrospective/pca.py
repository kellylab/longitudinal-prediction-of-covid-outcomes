from covidmonte import *
from covidmonte.ml import featurize_dataset, interpolate_dataset, stack_dataset, feature_columns, numerical_columns, boolean_columns, categorical_columns
import seaborn as sns
import os
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from mlxtend.plotting import plot_pca_correlation_graph
from tqdm import tqdm
import pandas as pd
from umap import UMAP

base_path = "data/plots/unsupervised/"

outcomes_columns = [
    'death', 'intubation', 'non_rebreather_mask', 'cpap_bpap', 'nasal_cannula',
    'ecmo',
    ]

colors = {
    "death": "#003f5c",
    "intubation": "#374c80",
    "non_rebreather_mask": "#7a5195",
    "cpap_bpap": "#bc5090",
    "nasal_cannula": "#ef5675",
    "ecmo": "#ff764a",
    "none": "#ffa600",
}

# Cluster all of them
df = get_retrospective_data()
vectorized, categorical_dict, means, variances = featurize_dataset(df)
interpolated = interpolate_dataset(vectorized, means, categorical_dict)
interpolated = interpolated[numerical_columns]
interpolated = interpolated.T.drop_duplicates().T
data, columns = stack_dataset(interpolated, categories_dict=categorical_dict)
filled = pd.DataFrame(data, columns=columns, index=df.index)
to_drop = filled.columns[filled.isna().any()]
if len(to_drop):
    filled = filled.drop(columns=to_drop)
    columns = [x for x in columns if x not in to_drop]
data = np.array(filled)
pca = PCA(n_components=5)
reduced = pca.fit_transform(filled)
outcomes = df[outcomes_columns].fillna(False)

with Plotter(os.path.join(base_path, f"pca.svg"), show=False) as ax:
    unannotated = outcomes.any(1) == False    
    ax.scatter(reduced[unannotated,0], reduced[unannotated,1], color=colors["none"], label="None", alpha=.3)
    for outcome_column in outcomes_columns:
        where = outcomes[outcome_column] == True
        ax.scatter(reduced[where,0], reduced[where,1], color=colors[outcome_column], label=outcome_column, alpha=.5)
    ax.set_title(f"PCA for Lab Values by Outcome for all Patients.")
    ax.legend()

umap = UMAP()
umap_reduced = umap.fit_transform(filled)
with Plotter(os.path.join(base_path, f"umap.svg"), show=False) as ax:
    unannotated = outcomes.any(1) == False
    ax.scatter(reduced[unannotated,0], reduced[unannotated,1], color=colors["none"], label="None", alpha=.3)
    for outcome_column in outcomes_columns:
        where = outcomes[outcome_column] == True
        ax.scatter(umap_reduced[where,0], umap_reduced[where,1], color=colors[outcome_column], label=outcome_column, alpha=.5)
    ax.set_title(f"UMAP for Lab Values by Outcome for all Patients.")
    ax.legend()



for study in tqdm(studies):

    df = get_retrospective_data(study=study)
    vectorized, categorical_dict, means, variances = featurize_dataset(df)
    interpolated = interpolate_dataset(vectorized, means, categorical_dict)
    interpolated = interpolated[numerical_columns]
    interpolated = interpolated.T.drop_duplicates().T
    data, columns = stack_dataset(interpolated, categories_dict=categorical_dict)
    filled = pd.DataFrame(data, columns=columns, index=df.index)
    to_drop = filled.columns[filled.isna().any()]
    if len(to_drop):
        filled = filled.drop(columns=to_drop)
        columns = [x for x in columns if x not in to_drop]
    data = np.array(filled)
    pca = PCA(n_components=5)
    reduced = pca.fit_transform(filled)
    outcomes = df[outcomes_columns].fillna(False)

    with Plotter(os.path.join(base_path, f"pca_{study}.svg"), show=False) as ax:
        unannotated = outcomes.any(1) == False
        ax.scatter(reduced[unannotated,0], reduced[unannotated,1], color=colors["none"], label="None", alpha=.5)
        for outcome_column in outcomes_columns:
            where = outcomes[outcome_column] == True
            ax.scatter(reduced[where,0], reduced[where,1], color=colors[outcome_column], label=outcome_column, alpha=.5)
        ax.set_title(f"PCA for Lab Values by Outcome for Study {study}.")
        ax.legend()

    umap = UMAP()
    umap_reduced = umap.fit_transform(filled)
    with Plotter(os.path.join(base_path, f"umap_{study}.svg"), show=False) as ax:
        unannotated = outcomes.any(1) == False
        ax.scatter(reduced[unannotated,0], reduced[unannotated,1], color=colors["none"], label="None", alpha=.5)
        for outcome_column in outcomes_columns:
            where = outcomes[outcome_column] == True
            ax.scatter(umap_reduced[where,0], umap_reduced[where,1], color=colors[outcome_column], label=outcome_column, alpha=.5)
        ax.set_title(f"UMAP for Lab Values by Outcome for Study {study}.")
        ax.legend()

    figure, correlation_matrix = plot_pca_correlation_graph(data, 
                                                            ["" for _ in columns],
                                                            dimensions=(1, 2, 3, 4, 5),
                                                            figure_axis_size=10)
    plt.savefig(os.path.join(base_path,f"correlation_circle_{study}.png"))
    #plt.show()
    plt.clf()