from covidmonte import *
from covidmonte.timeline import plot_timeline
import matplotlib.pyplot as plt
import os

df = get_retrospective_data()
dates = get_date_columns(df)

base_path = "data/plots/timelines"

for _, row in dates.iterrows():
    with Plotter(os.path.join(base_path,"{0}.svg".format(row['Patient_study_ID'])), show=False, figsize=(10,5)) as ax:
        plot_timeline(row, ax)