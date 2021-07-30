from covidmonte import *
import os
from statsmodels.stats.multitest import fdrcorrection
import pandas as pd
import seaborn as sns
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from scipy.stats import fisher_exact

base_path = "data/plots/associations_categorical"

# See what is associated with an outcome
outcomes = [
    'death', 'intubation', 'non_rebreather_mask', 'cpap_bpap', 'nasal_cannula',
    'cardiogenic_shock', 'myocarditis', 'sepsis', 'ards', 'ecmo',
    ]

boolean_factors = [
    'fever', 'cough', 'shortness_of_breath', 'fatigue', 'sore_throat', 'headache',
    'diarrhea', 'altered_mental_status', 'antipyretics', 'received_oral_meds_in_1st_24hr',
    'on_o2_at_presentation', 'aki', "cxr_bilateral_opacities", "cxr_interstitial", "cxr_unilateral_opacities",
    'pronation_treatment', 'glucose_6', 'nsaid', 'copd', 'asthma', 'hypertension', 'diabetes', 
    'pulmonary_dx', 'heart_disease', 'malignancy', 'ckd', 'hd', 'immunocompromised', 'hiv', 
    'other_comorbidity_bool', 'ace', 'arb',
]
 

df = get_retrospective_data(regenerate=True)
associations = pd.DataFrame(columns=['outcome', 'factor', 'p-value', 'q-value', 'odds-ratio'])
for outcome in outcomes:

    positive = df[df[outcome] == True]
    negative = df[df[outcome] == False]

    pvalues = []
    for factor in boolean_factors:

        positive_positive = sum(positive[factor] == True)
        positive_negative = sum(positive[factor] == False)
        negative_positive = sum(negative[factor] == True)
        negative_negative = sum(negative[factor] == False)

        test_matrix = pd.DataFrame({
            outcome: [positive_positive, positive_negative],
            f"not {outcome}": [negative_positive, negative_negative]
            },
            index = [factor, f"not {factor}"]
        )
        o, p = fisher_exact(test_matrix)
        pvalues.append({
            "outcome": outcome,
            "factor": factor,
            "p-value": p,
            "odds-ratio": o,
        })       

    if len(pvalues):

        a = pd.DataFrame(pvalues)
        a['q-value'] = fdrcorrection(a['p-value'])[1]
        associations = associations.append(a)

# Plot heatmap for q-values
q_heat = pd.DataFrame(index=boolean_factors, columns=outcomes)
for factor in boolean_factors:
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
auc_heat = pd.DataFrame(index=boolean_factors, columns=outcomes)
for factor in boolean_factors:
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
plt.title("Association Odds-Ratio")
plt.savefig(os.path.join(base_path, 'associations_or_heatmap.svg'))

# Plot AUC for values that are significant
sns.clustermap(auc_heat.where(significant==1).fillna(0.))
plt.title("Association Odds-Ratio")
plt.savefig(os.path.join(base_path, 'significant_or_heatmap.svg'))