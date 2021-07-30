from covidmonte import *
import os
from scipy.stats import mannwhitneyu
from statsmodels.stats.multitest import fdrcorrection
import pandas as pd
import seaborn as sns
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt

base_path = "data/plots/associations_labs"

# See what is associated with an outcome
outcomes = [
    'death', 'intubation', 'non_rebreather_mask', 'cpap_bpap', 'nasal_cannula',
    'cardiogenic_shock', 'myocarditis', 'sepsis', 'ards', 'ecmo',
    ]

numerical_factors = [
    "a1c",
    "cd4_count_most_recent",
    "cd4_percent_most_recent",
    "wbcadmac",
    "wbcpeakac",
    "wbcnadirac",
    "crpeakac",
    "cradmac",
    "bunadmac",
    "neutadmac",
    "neutnadirac",
    "lymphadmac",
    "lymphnadirac",
    "pltpeakac",
    "pltnadirac",
    "pltadmac",
    "astpeakac",
    "astadmac",
    "astadmac",
    "altadmac",
    "ldhpeakac",
    "ldhadmac",
    "procalpeakac",
    "procaladmac",
    "crppeakac",
    "crpadmac",
    "ddimeradmac",
    "ddimerpeakac",
    "inradmac",
    "inrpeakac",
    "fibrinoadmac",
    "fibrinopeakac",
    "ferritadmac",
    "ferritpeakac",
    "pttadmac",
    "pttpeakac",
    "ptadmac",
    "ptpeakac",
    "alkpadmac",
    "alkppeakac",
    "albadmac",
    "il6initac",
    "il6peakac",
    "eosadmac",
    "bpsystac",
    "bpdiastac",
    "tempinitac",
    "tempmaxac",
    "rrinitac",
    "pulseoxinitac",
]

df = get_retrospective_data(regenerate=True)
associations = pd.DataFrame(columns=['outcome', 'factor', 'mwu', 'p-value', 'q-value', 'auc'])
for outcome in outcomes:

    positive = df[df[outcome] == True]
    negative = df[df[outcome] == False]
    pvalues = []

    for factor in numerical_factors:

        positive_factor = positive[factor].dropna()
        negative_factor = negative[factor].dropna()
        if len(positive_factor)*len(negative_factor) != 0:

            result = mannwhitneyu(negative_factor, positive_factor)
            pvalues.append({
                "outcome": outcome,
                "factor": factor,
                "mwu": result.statistic,
                "p-value": result.pvalue,
                "auc": result.statistic / (len(positive_factor) * len(negative_factor))
            })
            try:
                os.mkdir(os.path.join(base_path, "violin", factor))
            except IOError:
                pass
            with Plotter(os.path.join(base_path, "violin", factor, f"{outcome}.svg"), show=False) as ax:

                sns.violinplot(positive_factor, color='orange', bins=25, ax=ax)
                sns.violinplot(negative_factor, color='green',bins=25, ax=ax)
                plt.setp(ax.collections, alpha=.5)
                ax.set_title(f"Association of {factor} vs. {outcome}")
                
                pos_label="{0} ({1})".format(outcome, len(positive_factor))
                neg_label="Not {0} ({1})".format(outcome, len(negative_factor))
                handles=ax.lines[::2]
                handles[0].set_color("orange")
                handles[1].set_color("green")

                ax.legend(handles=handles, labels=[pos_label, neg_label])

    if len(pvalues):
        a = pd.DataFrame(pvalues)
        a['q-value'] = fdrcorrection(a['p-value'])[1]
        associations = associations.append(a)

associations.to_csv(os.path.join(base_path, 'associations.csv'))

# Plot heatmap for q-values
q_heat = pd.DataFrame(index=numerical_factors, columns=outcomes)
for factor in numerical_factors:
    for outcome in outcomes:
        association = associations.loc[
            (associations['factor'] == factor) &
            (associations['outcome'] == outcome)
        ]
        try:
            q_heat.loc[factor][outcome] = association['q-value'].iloc[0]
        except:
            pass

q_heat = q_heat.astype(float).fillna(1.)

sns.clustermap(q_heat, figsize=(15,15))
plt.title("Association Q-Values")
plt.savefig(os.path.join(base_path, 'associations_q_heatmap.svg'))

significant = q_heat.applymap(lambda x: 1 if x<.05 else 0)  
sns.clustermap(significant, figsize=(15,15))
plt.title("Significant Associations")
plt.savefig(os.path.join(base_path, 'associations_heatmap.svg'))

# Plot heatmap for q-values
auc_heat = pd.DataFrame(index=numerical_factors, columns=outcomes)
for factor in numerical_factors:
    for outcome in outcomes:
        association = associations.loc[
            (associations['factor'] == factor) &
            (associations['outcome'] == outcome)
        ]
        try:
            auc_heat.loc[factor][outcome] = association['auc'].iloc[0]
        except:
            pass

auc_heat = auc_heat.astype(float).fillna(1.)

sns.clustermap(auc_heat, figsize=(15,15))
plt.title("Association AUC")
plt.savefig(os.path.join(base_path, 'associations_auc_heatmap.svg'))

# Plot AUC for values that are significant
sns.clustermap(auc_heat.where(significant==1).fillna(0.))
plt.title("Association AUC")
plt.savefig(os.path.join(base_path, 'significant_auc_heatmap.svg'))