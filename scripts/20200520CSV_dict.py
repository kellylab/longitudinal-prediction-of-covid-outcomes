# author: Dylan Festa
# Parsing the column names in the csv file
#... by stealing Saad's python dictionaries
# %%
from typing import Dict
import pandas as pd


# %%

identifying_columns = [
    "Patient_study_ID",
    "MRN",
    "Patient_study_ID_1",
]

demographic_columns = {
"Date of Birth": "dob",
"Age": "age",
"Sex (Female=1. Male=0)": "sex",
"Ethnicity (1=\"Hispanic/Latino\". 0= \"NOT hispanic/latino. . = unknown/missing)":"hispanic",
"Race (1=Black. 2=white. 3=other. = unknown/missing)": "race",
"Place of residence (nursing home/assisted living = 1. home=0. 2=other. . = unknown)": "residence",
"HCW (1=Y. 0=N. .=unknown)": "hcw",
"Smoking- Former or current (0=No. 1= Yes. . unkn)": "smoker",
"BMI": "bmi",
}

date_columns = {
    "Presentationdate1": "presentation_date1",
    "Dischargedate1": "discharge_date1",
    "Admissiondate2": "admission_date2",
    "Dischargedate2": "discharge_date2",
    "ICUadmissiondate1": "icu_admission_date_1",
    "ICUadmissiondate2": "icu_admission_date_2",
    "ICUdischargedate2": "icu_discharge_date_2",
    "SARS-CoV-2collectiondate1": "covid_collection_date_1",
    "SARS-CoV-2resultdate1": "covid_result_date_1",
    "SARS-CoV-2collectiondate2": "covid_collection_date_2",
    "SARS-CoV-2resultdate2": "covid_result_date_2",
    "SARS-CoV-2collectiondate3": "covid_collection_date_3",
    "SARS-CoV-2resultdate3": "covid_result_date_3",
    "Intubationdate1": "intubation_date_1",
    "Extubationdate1": "extubation_date_1",
    "Intubationdate2": "intubation_date_2",
    "Extubationdate2": "extubation_date_2",
    "Deathdate": "death_date",
    "wbcadmdateac": "wbc_admission_date",
    "cradmdateac": "creatinine_admission_date",
    "bunadmdateac": "bun_admission_date",
    "astadmdateac": "ast_admission_date",
    "ldhadmdateac": "ldh_admission_date",
    "crpadmdateac": "crp_admission_date",
    "ddimeradmdateac": "ddimer_admission_date",
    "inradmdateac": "inr_admission_date",
    "fibrinoaddatemac": "fibrinogen_admission_date",
    "ferritadmdateac": "ferritin_admission_date",
    "pttadmdateac": "ptt_admission_date",
    "CD4date": "cd4_date",
}

status_columns = {
  "Admitted or Outpt/ED (outpatient=0. ED=1. admit=2)": "admission_level",
  "DischargeDispo1 (0=home. 1=nursing home/assisted living/rehab 2=deceased. 3=other. .=unknown)": "discharge_destination_1",
  "DischargeDispo2 (0=home. 1=nursing home/assisted living/rehab 2=deceased. 3=other. .=unknown)": "discharge_destination_2",
  "DaysOfSymptomsBefore1stAdmission (unknown .. otherwise number)": "days_of_symptoms_before_1st_admission",
  "stillinpatient": "still_inpatient",
}

symptoms_columns = {
    "Fever (Yes=1. No=0. unknown=.)": "fever",
    "Cough": "cough",
    "SOB": "shortness_of_breath",
    "Fatigue": "fatigue",
    "Sore throat": "sore_throat",
    "Chills": "chills",
    "Headache": "headache",
    "Diarrhea": "diarrhea",
    "Othersymptoms": "other_symptoms",
    "Fever duration (days)- (>100.4 days)": "fever_duration",
}

vitals_columns = {
    "TempF - initial temp (or date of test collection)": "initial_temp",
    "TempF - max temp during admission": "max_temp_admission",
    "Systolic BP - first recorded": "systolic_bp",
    "Diastolic BP - first recorded ": "diastolic_bp",
    "RR - initial": "initial_rr",
    "SaO2 (please write as NUMBER)": "o2_saturation",
    "Lung exam results (wheezing. rales.rhonchi. egophony)": "lung_exam",
    "Altered Mental Status (Yes=1. No=0. unknown=.)": "altered_mental_status",
}

categorical_events_columns = {
    "Antipiretics- (Yes=1. No=0. unknown=.) ": "antipyretics",
    "Received oral medications in first 24 hours (Yes=1. No=0. unknown = .)": "received_oral_meds_in_1st_24hr",
    "On oxygen at presentation (Yes=1. No=0. unknown=.)": "on_o2_at_presentation",
    "Intubations (0=No. 1=Yes. Unknown= 0)": "intubation",
    "Hi-flow (0=no. 1=yes. Unk= 0)": "hi_flow",
    "NonRebreather Mask (N=no. 1=yes. Unk= 0)": "non_rebreather_mask",
    "(CPAP/BPAP) (1/0)": "cpap_bpap",
    "nasal cannula (1/0)": "nasal_cannula",
    "AKI (Yes=1. No=0. unknown=.)": "aki",
    "Concurrent pathogen infection (describe in free text) (bacterial. viral. fungal. etc)": "concurrent_pathogen_infection",
    "Sepsis/septic shock?": "sepsis",
    "Cardiogenic shock": "cardiogenic_shock",
    "Myocarditis": "myocarditis",
    "Cardiac arrest (Yes=1. No=0. unknown=.)": "cardiac_arrest",
    "ARDS (Yes=1.No=0. unknown=.)": "ards",
    "ECMO (Yes=1. No=0. unknown=.)": "ecmo",
    "Other Complications free text (stroke. heart failure. renal failure. pulmonary embolism. etc)": "other_complications",
    "readmission": "readmission",
    "composite": "composite",
    "death": "death",
    'SARS-CoV-2finalresult1': 'covid_result_1',
    'SARS-CoV-2finalresult2': 'covid_result_2',
    'SARS-CoV-2finalresult3': 'covid_result_3',
}

radiology_columns = {
    "Admission x-ray (paste text)": "admission_xray",
    "CXR-BilatOpacities": "cxr_bilateral_opacities",
    "CXR-Interstitial": "cxr_interstitial",
    "CXR-UnilatOpacities": "cxr_unilateral_opacities",
    "POCUSlunginitial Free text": "initial_lung_ultrasound",
    "POCUSheartinitial free text": "initial_heart_ultrasound",
}

comorbidities_columns = {
    "COPD (0=No. 1= Yes. 999=unknown)": "copd",
    "Asthma (0=No. 1= Yes. 999=unknown)": "asthma",
    " Hypertension(0=No. 1= Yes. .=Unknown)": "hypertension",
    "Diabetes (complicated by CKD. PVD. CHF/ischemic cardiomyopathy. OR uncomplicated)(0=No. 1= Yes. 999=Unknown)": "diabetes",
    "Pulmonary disease (COPD. asthma. emphysema. bronchiectasis. pulmonary hypertension)(0=No. 1= Yes. 999=Unknown)": "pulmonary_dx",
    " Heart disease (CAD. hx of CABG or PCI. CHF. AICD": "heart_disease",
    "Malignancy  (within 2 years or receiving immunosuppressive treatment)(0=No. 1= Yes. 999=Unknown)": "malignancy",
    "Chronic kidney disease(0=No. 1= Yes. 999=Unknown)": "ckd",
    "HD (Yes=1. No=0. unknown=.)": "hd",
    "Immunocompromised state (eg: steroids. monoclonal antibod1 tx for asthma/RA. transplant)(0=No. 1= Yes. 999=Unknown)": "immunocompromised",
    "HIV(0=No. 1= Yes. 999=Unknown)": "hiv",
    "Other comorbidity(0=No. 1= Yes. 999=Unknown)": "other_comorbidity_bool",
    "Other comorbidity- free text": "other_comorbidity",
    "ACE (1=yes. 0=no. .=unknown)": "ace",
    "ARB (1=yes. 0=no. .=unknown)": "arb",
}

treatments_columns = {
    "Chloroquinedays": "chloroquine_days",
    "Hydroxychloroquinedays": "hydroxychloroquine_days",
    "Kaletra (Lopinavir/Ritonavir) days": "kaletra_days",
    "Remdesivir-compastionate days": "remdesivir_compassionate_days",
    "Remdesivir- clinical trial days": "remdesivir_clinical_trial_days",
    "OtherTrial_free text": "other_trial",
    "Pressors days": "pressors_days",
    "pronation (Y=1. N=0. unknown=.) - search in notes": "pronation_treament",
    "Other IV antibiotics (new columns?)": "other_iv_abx",
    "Azithromycindays": "azithromycin_days",
    "Glucose-6 (Yes=1. No=0. missing/unknown=.)": "glucose_6",
    "Glucocorticoids_freetext": "glucocorticoids",
    "NSAID (Yes=1. No=0. unknown=.)": "nsaid",
}

labs_columns = {
    "A1C%": "aic",
    "CD4count_mostrecent": "cd4_count_most_recent",
    "CD4%_mostrecent": "cd4_percent_most_recent",
    "wbcadmac": "wbcadmac",
    "wbcpeakac": "wbcpeakac",
    "wbcnadirac": "wbcnadirac",
    "crpeakac": "crpeakac",
    "cradmac":  "cradmac",
    "bunadmac":  "bunadmac",
    "neutadmac": "neutadmac",
    "neutnadirac": "neutnadirac",
    "lymphadmac": "lymphadmac",
    "lymphnadirac": "lymphnadirac",
    "pltpeakac": "pltpeakac",
    "pltnadirac": "pltnadirac",
    "pltadmac": "pltadmac",
    "astpeakac": "astpeakac",
    "astadmac": "astadmac",
    "astadmac": "astadmac",
    "altadmac": "altadmac",
    "ldhpeakac": "ldhpeakac",
    "ldhadmac": "ldhadmac",
    "procalpeakac": "procalpeakac",
    "procaladmac": "procaladmac",
    "crppeakac": "crppeakac",
    "crpadmac": "crpadmac",
    "ddimeradmac": "ddimeradmac",
    "ddimerpeakac": "ddimerpeakac",
    "inradmac": "inradmac",
    "inrpeakac": "inrpeakac",
    "fibrinoadmac": "fibrinoadmac",
    "fibrinopeakac": "fibrinopeakac",
    "ferritadmac": "ferritadmac",
    "ferritpeakac": "ferritpeakac",
    "pttadmac": "pttadmac",
    "pttpeakac": "pttpeakac",
    "ptadmac": "ptadmac",
    "ptpeakac": "ptpeakac",
    "alkpadmac": "alkpadmac",
    "alkppeakac": "alkppeakac",
    "albadmac": "albadmac",
    "il6initac": "il6initac",
    "il6peakac": "il6peakac",
    "eosadmac": "eosadmac",
    "g6pd-def1-norml0-inter2": "g6pd-def1-norml0-inter2",
    "bpsystac": "bpsystac",
    "bpdiastac": "bpdiastac",
    "tempinitac": "tempinitac",
    "tempmaxac": "tempmaxac",
    "rrinitac": "rrinitac",
    "pulseoxinitac": "pulseoxinitac",
}

missing_columns=["ICUdischargedate1",
 "neutadmdateac",
 "lymphpeakac",
 "altpeakac",
 "procaladmdateac",
 "il6initdateac",
 "qsofaams",
 "qsofabp",
 "qsofarr",
 "qsofa"]

# %%

allkeys = []
allvals = []

for k in identifying_columns:
    allkeys.append(k)
    allvals.append(k)
for k in missing_columns:
    allkeys.append(k)
    allvals.append(k)
for (k,v) in demographic_columns.items():
    allkeys.append(k)
    allvals.append(v)
for (k,v) in date_columns.items():
    allkeys.append(k)
    allvals.append(v)
for (k,v) in status_columns.items():
    allkeys.append(k)
    allvals.append(v)
for (k,v) in symptoms_columns.items():
    allkeys.append(k)
    allvals.append(v)
for (k,v) in vitals_columns.items():
    allkeys.append(k)
    allvals.append(v)
for (k,v) in categorical_events_columns.items():
    allkeys.append(k)
    allvals.append(v)
for (k,v) in radiology_columns.items():
    allkeys.append(k)
    allvals.append(v)
for (k,v) in comorbidities_columns.items():
    allkeys.append(k)
    allvals.append(v)
for (k,v) in treatments_columns.items():
    allkeys.append(k)
    allvals.append(v)
for (k,v) in labs_columns.items():
    allkeys.append(k)
    allvals.append(v)

# %%

keys_oldnew = pd.DataFrame({'key_raw':allkeys, 'key_new':allvals })

savekeys = "../data/confidential/keys_list.csv"

keys_oldnew.to_csv(savekeys)



# %%
