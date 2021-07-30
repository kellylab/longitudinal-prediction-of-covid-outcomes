import pandas as pd
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from typing import Dict
import math
from .clean_data import *

identifying_columns = [
    "Patient_study_ID",
    "MRN",
    "Patient_study_ID.1",
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
    'ICUdischargedate1': 'icu_discharge_date_1',
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
    "pronation (Y=1. N=0. unknown=.) - search in notes": "pronation_treatment",
    "Other IV antibiotics (new columns?)": "other_iv_abx",
    "Azithromycindays": "azithromycin_days",
    "Glucose-6 (Yes=1. No=0. missing/unknown=.)": "glucose_6",
    "Glucocorticoids_freetext": "glucocorticoids",
    "NSAID (Yes=1. No=0. unknown=.)": "nsaid",
}

labs_columns = {
    "A1C%": "a1c",
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

def clean_demographics(df: pd.DataFrame) -> pd.DataFrame:
    
    # Clean DOB
    df['dob'] = df['dob'].apply(pd.to_datetime)
    age = df['age'].fillna(0.)
    age[age == 0] = math.nan
    df['age'] = age

    def sex(s):
        return {
            1. : "female",
            0. : "male",
        }.get(s)

    df['sex'] = df['sex'].apply(sex)

    df['hispanic'] = df['hispanic'].apply(true_false)

    def race(r):
        return {
            1 : "black",
            2 : "white",
            3 : "unknown",
        }.get(r)

    df['race'] = df['race'].apply(race)

    def residence(r):
        return {
            0: 'home',
            1: 'assisted_living',
            2: 'other',
            '1 (lives part time at group home)': 'part_time_assisted_living',
        }.get(r)
    
    df['residence'] = df['residence'].apply(residence)

    df['hcw'] = df['hcw'].apply(true_false)

    df['smoker'] = df['smoker'].apply(true_false)

    def bmi(b):
        try:
            return float(b)
        except:
            return np.nan


    df['bmi'] = df['bmi'].apply(bmi)

    return df

def clean_dates(df: pd.DataFrame) -> pd.DataFrame:

    for col in date_columns.values():
        df[col] = pd.to_datetime(df[col], errors='coerce')
    
    return df

def clean_status(df: pd.DataFrame) -> pd.DataFrame:

    def admission_level(a):
        return {
            0.: 'outpatient',
            1.: 'ed',
            2.: 'admit'
        }.get(a)


    df['admission_level'] = df['admission_level'].apply(admission_level)

    def destination(d):
        return {
            0: 'home',
            1: 'assisted_living',
            '1 (group home)': 'assisted_living',
            2: 'deceased',
            3: 'other',
            '3- AMA': 'other',
            'INPATIENT': 'other',
            '3-eloped': 'other',
        }.get(d)
    
    df['discharge_destination_1'] = df['discharge_destination_1'].apply(destination)
    df['discharge_destination_2'] = df['discharge_destination_2'].apply(destination)
    
    def days_before(d):
        try:
            return float(d)
        except:
            if d == '1st-2/2nd-2':
                return 2.
            elif d == 'NOT COVID POSITIVE (1)':
                return 1.
            else:
                return np.nan
    
    df['days_of_symptoms_before_1st_admission'] = df['days_of_symptoms_before_1st_admission'].apply(days_before)
    df['still_inpatient'] = df['still_inpatient'].apply(true_false)

    return df

def clean_symptoms(df: pd.DataFrame) -> pd.DataFrame:

    for col in ['fever','cough','shortness_of_breath',"fatigue","sore_throat","chills","headache","diarrhea"]:
        df[col] = df[col].apply(true_false)
    
    df["fever_duration"] = df["fever_duration"].apply(lambda x: coerce_type(x,float))

    return df

def clean_vitals(df: pd.DataFrame) -> pd.DataFrame:

    for col in ['initial_temp', 'max_temp_admission', 'systolic_bp', 'diastolic_bp', 'initial_rr', 'o2_saturation']:
        df[col] = df[col].apply(lambda x: coerce_type(x, float))
    
    df['altered_mental_status'] = df['altered_mental_status'].apply(true_false)

    return df

def clean_categorical_events(df: pd.DataFrame) -> pd.DataFrame:

    for col in [
        'antipyretics', 'received_oral_meds_in_1st_24hr', 'on_o2_at_presentation', 
        'intubation', "hi_flow", "non_rebreather_mask", "cpap_bpap", "nasal_cannula",
        "aki", "sepsis", "cardiogenic_shock", "myocarditis", "cardiac_arrest", "ards",
        "ecmo", "readmission", "death", 'covid_result_1', 'covid_result_2', 'covid_result_3',
    ]:
        df[col] = df[col].apply(true_false)

    df['concurrent_pathogen_infection_bool'] = df['concurrent_pathogen_infection'].apply(str2bool)

    return df

def clean_radiology_columns(df: pd.DataFrame) -> pd.DataFrame:

    for col in [
        "cxr_bilateral_opacities", "cxr_interstitial", "cxr_unilateral_opacities"
    ]:
        df[col] = df[col].apply(true_false)
    
    return df

def clean_comorbidities_columns(df: pd.DataFrame) -> pd.DataFrame:

    for col in [
        "copd", "asthma", "hypertension", "diabetes", "pulmonary_dx",
        "heart_disease",  "malignancy", "ckd", "hd", "immunocompromised",
        "hiv", "other_comorbidity_bool", "ace", "arb",
    ]:
        df[col] = df[col].apply(true_false)
    
    return df

def clean_treatments_columns(df: pd.DataFrame) -> pd.DataFrame:

    for col in [
        "pronation_treatment", "glucose_6", "nsaid",
    ]:
        df[col] = df[col].apply(true_false)
        
    df['remdesivir_clinical_trial_days'] = df['remdesivir_clinical_trial_days'].map({'1 (2 doses)': 1.})
    
    for col in [
        "chloroquine_days", "hydroxychloroquine_days", "kaletra_days", 
        "remdesivir_compassionate_days", "remdesivir_clinical_trial_days", 
        "other_trial", "pressors_days", "azithromycin_days",
    ]:
        df[col] = df[col].apply(lambda x: coerce_type(x, float))

    return df

def clean_labs_columns(df: pd.DataFrame) -> pd.DataFrame:

    for col in [
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
    ]:
        df[col] = df[col].apply(lambda x: coerce_type(x, float))

    def clean_a1c(x):
        """
        The rows in the a1c column are either:
            - a number
            - the values <4 or >14 (these are extreme values of HgA1C)
            - a number with a date next to them
            - a '.' (means na)
        In general, the A1C values fall in the range of 4-14.
        We map <4 and >14 to 4 and 14 respectively.
        We parse out the dates in the corresponding rows that everything is a float.
        """
        if x == '.':
            return np.nan
        try:
            return float(x)
        except:
            pass

        # Parse out the number in the string which represents the A1C value
        tokens = [' ', '-', '>', '<', '01']
        splits = [x]
        for token in tokens:
            new_splits = []
            for split in splits:
                new_splits.extend(split.split(token))
            splits = new_splits
        
        # Splits is a list and one of the elements in the list will be a
        # floating point number
        for split in splits:
            try:
                return float(split)
            except:
                pass
        
        raise ValueError # The above should have covered all edge cases.

    
    df['a1c'] = df['a1c'].apply(clean_a1c)

    return df

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans up the data by renaming columns, etc.
    """
    df['patient_study_id'] = df["Patient_study_ID"]
    df['study_member'] = df['Study member'].fillna("no study")
    df.index = df["patient_study_id"]
    df = df.drop(columns=['MRN', "patient_study_id", "Patient_study_ID", "Patient_study_ID.1", 'Study member']) # anonymize

    df = rename(df, demographic_columns)
    df = rename(df, date_columns)
    df = rename(df, status_columns)
    df = rename(df, symptoms_columns)
    df = rename(df, vitals_columns)
    df = rename(df, categorical_events_columns)
    df = rename(df, radiology_columns)
    df = rename(df, comorbidities_columns)
    df = rename(df, treatments_columns)
    df = rename(df, labs_columns)

    df = clean_demographics(df)
    df = clean_dates(df)
    df = clean_status(df)
    df = clean_symptoms(df)
    df = clean_vitals(df)
    df = clean_categorical_events(df)
    df = clean_radiology_columns(df)
    df = clean_comorbidities_columns(df)
    df = clean_treatments_columns(df)
    df = clean_labs_columns(df)

    return df