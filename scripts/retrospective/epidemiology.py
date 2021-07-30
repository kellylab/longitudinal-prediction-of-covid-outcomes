from covidmonte import *
import matplotlib.pyplot as plt
import os
import pandas as pd
from statsmodels.graphics.mosaicplot import mosaic
import seaborn as sns
sns.set(style="whitegrid", palette="muted")

base_path = "data/plots/epidemiology"
df = get_retrospective_data()

# Age histograms by whether or not patient died.
alive = df[df['death']!=True]
died = df[df['death'] == True]

with Plotter(os.path.join(base_path, "age_histogram.svg")) as ax:
    died.hist('age', ax=ax, alpha=.5, density=True, label="Deceased")
    alive.hist('age', ax=ax, alpha=.5, density=True, label="Alive")
    ax.set_title("Age Distribution by Survivor Status")
    ax.legend()

# BMI histograms by survival
#bmi_Deceased = pd.Series(float(x) for x in died['BMI'] if x != '.')
#bmi_alive = pd.Series(float(x) for x in alive['BMI'] if x != '.')

with Plotter(os.path.join(base_path, "bmi_histogram.svg")) as ax:
    died.hist('bmi', ax=ax, alpha=.5, density=True, label="Deceased")
    alive.hist('bmi', ax=ax, alpha=.5, density=True, label="Alive")
    ax.set_title("BMI Distribution by Survivor Status")
    ax.legend()

# Gender histograms by survival
male = df[df['sex']=='male']
female = df[df['sex']=='female']

with Plotter(os.path.join(base_path, "sex_histogram.svg")) as ax:
    male.hist('age', ax=ax, alpha=.5, density=True, label="Male")
    female.hist('age', ax=ax, alpha=.5, density=True, label="Female")
    ax.set_title("Age Distribution by Sex")
    ax.legend()

# Correspondence Analysis for Demographics

df['hispanic'] = df['hispanic'].map({True:'hispanic', False:'not hispanic'})
df['hcw'] = df['hcw'].map({True:'hcw', False:'not hcw'})
df['smoker'] = df['smoker'].map({True:'smoker', False:'non-smoker'})

with Plotter(os.path.join(base_path, "demographics.svg"), figsize=(10,10)) as ax:
    mosaic(df, ['sex', 'race', 'hispanic', 'smoker'], ax=ax, title="Demographic Breakdown by Smoking Status")
with Plotter(os.path.join(base_path, "demographics2.svg"), figsize=(10,10)) as ax:
    mosaic(df, ['sex', 'race', 'hispanic', 'hcw'], ax=ax, title="Demographic Breakdown by Healthcare Worker Status")


# significance test by common attributes
# temporal histogram of patient presence in hospital
# predict survival odds by admission statistics
# survival curves