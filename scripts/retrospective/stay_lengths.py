from covidmonte import *
import os

df = get_retrospective_data(regenerate=True)
base_path = "data/plots/stay_lengths"

# Get distribution of stay lengths
deceased = df[df['death']==True]
deceased_time = (deceased['death_date'] - deceased['presentation_date1']).map(lambda x: x.days)
deceased_time = deceased_time[deceased_time<200] # Eliminate outliers

with Plotter(os.path.join(base_path, 'stay_length.svg'), figsize=(10,10)) as ax:
    deceased_time.hist(ax=ax, label="Deceased")
    ax.set_title("Distribution of Number of Days from Presentation to Death")
    ax.set_xlabel("Days")