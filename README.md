# covid-montefiore
Analysis of Covid patients in the Bronx at Montefiore Medical Center

**Contents:**
- [Analysis](#analysis)
- [Usage](#usage)
- [Dataset Cleaning](#dataset-cleaning)

# Analyses

# Usage

You must have a file called `COVID19_RETROSPECTIVE_DATA5.15.xlsx` in the folder
`data/raw`

*** Note: This file contains confidential patient information and is not available in the public source for this paper. ***

## To load the dataset (into python)
  
```
from covidmonte import get_retrospective_data
df = get_retrospective_data()
```
The first time you do this, the 'cleaned' dataset will be generated and stored
as a CSV file
in `data/confidential`. Afterwards, this dataset will be loaded.

## To load the dataset (other languages)

Follow the instructions above for python to generate the processed CSV file (or
get it from someone). Then load that CSV file into the tool of your choice.

## Additional utilities (Python)

There is a context manager called `Plotter` which generates a matplotlib ax and
automatically saves the resulting figure on exit. Here's an example:

```
df = get_retrospective_data()
with Plotter('histogram.svg', show=False) as ax:
  df.hist('age', ax=ax)
  ax.set_title("Distribution of Patient Ages")
```
This will generate the following histogram saved as `histogram.svg`:

![histogram](histogram.svg)

This is a very wide dataset with 182 columns. To make this easier to work with,
you can extract a subset of the data using predefined lists of columns in the
`covidmonte` package:

- demographic_columns
- date_columns
- status_columns
- symptoms_columns
- vitals_columns
- categorical_events_columns
- radiology_columns
- comorbidities_columns
- treatments_columns
- labs_columns



# Dataset Cleaning

The script scripts/clean_dataset.py converts the raw data stored in
`data/raw/COVID19_RETROSPECTIVE_5.15.csv` to a DataFrame with the columns cleaned
up as described below. The raw data is in .gitignore, so you will have to get it
yourself and put it inside your version of the repo.

Whenever a column name is changed in the cleaned version of the dataset, its new
name is listed after an arrow (->).
All columns in the cleaned version are lower-case.

## Identifying Columns

- Patient_study_ID -> id
- MRN -> mrn
- Patient_study_ID.1 -> id2

## Demographic Columns

- Date of Birth -> dob
- Age
- Sex (Female=1. Male=0) -> sex
- Ethnicity (1="Hispanic/Latino". 0= "NOT hispanic/latino. . = unknown/missing)
  -> ethnicity
- Race (1=Black. 2=white. 3=other. = unknown/missing) -> race
- Place of residence (nursing home/assisted living = 1. home=0. 2=other. . =
  unknown) -> residence
- HCW (1=Y. 0=N. .=unknown) -> hcw
- Smoking- Former or current (0=No. 1= Yes. . unkn) -> smoking
- BMI

## Date Columns

- Presentationdate1
- Dischargedate1
- Admissiondate2
- Dischargedate2
- ICUadmissiondate1
- ICUadmissiondate2
- ICUdischargedate2
- SARS-CoV-2collectiondate1
- SARS-CoV-2resultdate1
- SARS-CoV-2collectiondate2
- SARS-CoV-2resultdate2
- SARS-CoV-2collectiondate3
- SARS-CoV-2resultdate3
- Intubationdate1
- Extubationdate1
- Intubationdate2
- Extubationdate2
- Deathdate
- wbcadmdateac
- cradmdateac
- bunadmdateac
- astadmdateac
- ldhadmdateac
- crpadmdateac
- ddimeradmdateac
- inradmdateac
- fibrinoaddatemac
- ferritadmdateac
- pttadmdateac
- CD4date

## Admission Status Info

- Admitted or Outpt/ED (outpatient=0. ED=1. admit=2) -> admission
- DischargeDispo1 (0=home. 1=nursing home/assisted living/rehab 2=deceased.
  3=other. .=unknown) -> discharge_destination1
- DischargeDispo2 (0=home. 1=nursing home/assisted living/rehab 2=deceased.
  3=other. .=unknown) -> discharge_destination2
- DaysOfSymptomsBefore1stAdmission (unknown .. otherwise number) -> days_of_symptoms_before_1st_admission
- stillinpatient

## Symptoms
- Fever (Yes=1. No=0. unknown=.) -> fever
- Cough
- SOB
- Fatigue
- Sore throat
- Chills
- Headache
- Diarrhea
- Othersymptoms
- Fever duration (days)- (>100.4 days) -> fever_duration

## Vitals

- TempF - initial temp (or date of test collection) -> initial_temp
- TempF - max temp during admission -> max_temp
- Systolic BP - first recorded -> 1stsystolic_bp
- Diastolic BP - first recorded -> 1stdiastolic_bp
- RR - initial -> initial_rr
- SaO2 (please write as NUMBER) -> sao2
- Lung exam results (wheezing. rales.rhonchi. egophony) -> lung_exam

## Categorical Events

These are events that took place but are not associated with a date.

- Antipiretics- (Yes=1. No=0. unknown=.) -> antipyretics
- Received oral medications in first 24 hours (Yes=1. No=0. unknown = .) -> oral_medication_in_1st_24hr
- On oxygen at presentation (Yes=1. No=0. unknown=.) -> on_o2_at_presentation
- Altered Mental Status (Yes=1. No=0. unknown=.) -> altered_mental_status
- Intubations (0=No. 1=Yes. Unknown= 0) -> intubated
- Hi-flow (0=no. 1=yes. Unk= 0) -> hiflow
- NonRebreather Mask (N=no. 1=yes. Unk= 0) -> non_rebreather_mask
- CPAP/BPAP) (1/0) -> cpap
- nasal cannula (1/0) -> nasal_cannula
- AKI (Yes=1. No=0. unknown=.) -> aki
- Concurrent pathogen infection (describe in free text) (bacterial. viral.
  fungal. etc) -> concurrent_pathogen_infection
- Sepsis/septic shock? -> sepsis
- Cardiogenic shock -> cardiogenic_shock
- Myocarditis -> myocarditis
- Cardiac arrest (Yes=1. No=0. unknown=.) -> cardiac_arrest
- ARDS (Yes=1.No=0. unknown=.) -> ards
- ECMO (Yes=1. No=0. unknown=.) -> ecmo
- Other Complications free text (stroke. heart failure. renal failure. pulmonary
  embolism. etc) -> other_complications
- readmission
- qsofaams
- qsofabp
- qsofarr
- qsofa
- composite
- death

## Radiology

- Admission x-ray (paste text) -> admission_cxr
- CXR-BilatOpacities -> cxr_bilateral_opacities
- CXR-Interstitial -> cxr_interstitial
- CXR-UnilatOpacities -> cxr_unilateral_opacities
- POCUSlunginitial Free text -> poc_us_lung_initial
- POCUSheartinitial free text -> poc_us_heart_initial

## Comorbidities

- COPD (0=No. 1= Yes. 999=unknown) -> copd
- Asthma (0=No. 1= Yes. 999=unknown) -> asthma
-  Hypertension(0=No. 1= Yes. .=Unknown) -> htn
-  Diabetes (complicated by CKD. PVD. CHF/ischemic cardiomyopathy. OR
   uncomplicated)(0=No. 1= Yes. 999=Unknown) -> diabetes
- Pulmonary disease (COPD. asthma. emphysema. bronchiectasis. pulmonary
  hypertension)(0=No. 1= Yes. 999=Unknown) -> pulmonary_dx
-  Heart disease (CAD. hx of CABG or PCI. CHF. AICD -> heart_dx
-  Malignancy  (within 2 years or receiving immunosuppressive treatment)(0=No.
   1= Yes. 999=Unknown) -> malignancy
- Chronic kidney disease(0=No. 1= Yes. 999=Unknown) -> ckd
- HD (Yes=1. No=0. unknown=.) -> hd
- Immunocompromised state (eg: steroids. monoclonal antibod1 tx for asthma/RA.
  transplant)(0=No. 1= Yes. 999=Unknown) -> immunocompromised
- HIV(0=No. 1= Yes. 999=Unknown) -> hiv
- Other comorbidity(0=No. 1= Yes. 999=Unknown) -> other_comorbidity
- Other comorbidity- free text -> other_comorbidity_text
- ACE (1=yes. 0=no. .=unknown) -> ace
- ARB (1=yes. 0=no. .=unknown) -> arb

## Labs

- A1C%
- CD4count_mostrecent
- CD4%_mostrecent
- wbcadmac
- wbcpeakac
- wbcnadirac
- crpeakac
- cradmac
- bunadmac
- neutadmac
- neutnadirac
- lymphadmac
- lymphnadirac
- pltpeakac
- pltnadirac
- pltadmac
- astpeakac
- astadmac
- altpeakac
- altadmac
- ldhpeakac
- ldhadmac
- procalpeakac
- procaladmac
- crppeakac
- crpadmac
- ddimeradmac
- ddimerpeakac
- inradmac
- inrpeakac
- fibrinoadmac
- fibrinopeakac
- ferritadmac
- ferritpeakac
- pttadmdateac
- pttadmac
- pttpeakac
- ptadmac
- ptpeakac
- alkpadmac
- alkppeakac
- albadmac
- il6initac
- il6peakac
- eosadmac
- g6pd-def1-norml0-inter2
- bpsystac
- bpdiastac
- tempinitac
- tempmaxac
- rrinitac
- pulseoxinitac
- readmission
- qsofaams
- qsofabp
- qsofarr
- qsofa

## Treatments

- Chloroquinedays -> chloroquine_days
- Hydroxychloroquinedays -> hydroxychloroquine_days
- Kaletra (Lopinavir/Ritonavir) days -> kaletra_days
- Remdesivir-compastionate days -> remdesivir_compassionate_days
- Remdesivir- clinical trial days -> remdesivir_clinical_trial_days
- OtherTrial_free text -> other_trial
- Pressors days -> pressors_days
- pronation (Y=1. N=0. unknown=.) - search in notes -> pronation
- Other IV antibiotics (new columns?) -> other_iv_abx
- Azithromycindays
- Glucose-6 (Yes=1. No=0. missing/unknown=.)
- Glucocorticoids_freetext
- NSAID (Yes=1. No=0. unknown=.)