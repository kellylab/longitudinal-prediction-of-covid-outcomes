from covidmonte import *
import seaborn as sns
import os
import matplotlib.pyplot as plt

base_path = "data/plots/exploration"

df = get_retrospective_data()

outcomes_columns = [
    'death', 'intubation', 'non_rebreather_mask', 'cpap_bpap', 'nasal_cannula',
    'ecmo',
    ]

outcomes = (df[outcomes_columns].dropna() == True).transpose()

sns.clustermap(outcomes)
plt.savefig(os.path.join(base_path, "outcomes.svg"))