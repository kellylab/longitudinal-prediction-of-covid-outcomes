from covidmonte import *
import os
from scipy.stats import mannwhitneyu
from statsmodels.stats.multitest import fdrcorrection
import pandas as pd
import seaborn as sns
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from datetime import datetime
from pandas import Timestamp
from tqdm import tqdm
import numpy as np

base_path = "data/plots/dates"

# See what is associated with an outcome
outcomes = [
    'death', 'intubation', 'non_rebreather_mask', 'cpap_bpap', 'nasal_cannula',
    'cardiogenic_shock', 'myocarditis', 'sepsis', 'ards', 'ecmo',
    ]

numerical_factors = [
    'initial_temp',
    'max_temp_admission',
    'systolic_bp',
    'initial_rr',
    'o2_saturation',
    "chloroquine_days", 
    "hydroxychloroquine_days", 
    "kaletra_days", 
    "remdesivir_clinical_trial_days", 
    "pressors_days", 
    "azithromycin_days",
]

df = get_retrospective_data()
associations = pd.DataFrame(columns=['outcome', 'factor', 'mwu', 'p-value', 'q-value', 'auc'])

dw = pd.DataFrame(columns=date_columns)
dd = pd.DataFrame(columns=date_columns)

for date_column in tqdm(date_columns):

    df['year_month_week'] = df[date_column].apply( # Drop the day so that patients are grouped by month.
        lambda x: pd.to_datetime(datetime(year=x.year, month=x.month, day=int(x.day/7)+1)
        if x is not pd.NaT 
        else x
        )
    )

    groups = {t[0]: t[1] for t in df.groupby('year_month_week')}
    counts = pd.DataFrame([{"Block": t, "Count": len(v)} for t,v in groups.items()]).set_index("Block")
    counts.to_csv(os.path.join(base_path,f"weekly_numbers_{date_column}.csv"))

    with Plotter(os.path.join(base_path,f"weekly_patients_{date_column}.svg"), figsize=(20,20), show=False) as ax:
        counts.plot.barh(ax=ax)
        ax.set_title(f"Counts of {date_column} by Week.")

    coco = counts.rename(columns={"Count": date_column})
    dw = dw.append(coco)
    
    daily_groups = {t[0]: t[1] for t in df.groupby(date_column)}
    daily_counts = pd.DataFrame([{"Block": t, "Count": len(v)} for t,v in daily_groups.items()]).set_index("Block")
    daily_counts.to_csv(os.path.join(base_path,f"daily_numbers_{date_column}.csv"),index=False)

    with Plotter(os.path.join(base_path,f"daily_patients_{date_column}.svg"), figsize=(20,20), show=False) as ax:
        daily_counts.plot.barh(ax=ax)
        ax.set_title(f"Counts of {date_column} by Day.")

    coco = daily_counts.rename(columns={"Count": date_column})
    dd = dd.append(coco)

dw = dw.fillna(0)
dd = dd.fillna(0)

dww = pd.DataFrame({date: dw[dw.index==date].sum() for date in set(dw.index)}).T.sort_index() 
ddd = pd.DataFrame({date: dd[dd.index==date].sum() for date in set(dd.index)}).T.sort_index() 

with Plotter(os.path.join(base_path, "weekly_counts.svg"), figsize=(20,20), show=False) as ax:
    np.log(dww+1).plot.barh(alpha=.6, ax=ax)
    ax.set_title("Events by Week")
    ax.set_xlabel("Log # Events")
    ax.set_ylabel("Week")

with Plotter(os.path.join(base_path, "daily_counts.png"), figsize=(20,20), show=False) as ax:
    np.log(ddd+1).plot.barh(alpha=.6, ax=ax, fontsize=14)
    ax.set_title("Events by Day", fontsize=14)
    ax.set_xlabel("Log # Events", fontsize=14)
    ax.set_ylabel("Day", fontsize=14)