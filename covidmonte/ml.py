# This file contains utilities for pre-processing related to ML
from typing import Tuple, List, Dict
from bidict import bidict
import pandas as pd
from itertools import count
import numpy as np
from . import eap

# Update

retrospective_boolean_columns = [
    "hispanic",
    "hcw",
    "smoker",
    "still_inpatient",
    "fever",
    "cough",
    "shortness_of_breath",
    "fatigue",
    "sore_throat",
    "chills",
    "headache",
    "diarrhea",
    "altered_mental_status",
    "death",
    'covid_result_1',
    'covid_result_2',
    'covid_result_3',
    "readmission",
    "antipyretics",
    "received_oral_meds_in_1st_24hr",
    "on_o2_at_presentation",
    "intubation",
    "hi_flow",
    "non_rebreather_mask",
    "cpap_bpap",
    "nasal_cannula",
    "aki",
    "concurrent_pathogen_infection_bool",
    "sepsis",
    "cardiogenic_shock",
    "myocarditis",
    "cardiac_arrest",
    "ards",
    "ecmo",
    "cxr_bilateral_opacities",
    "cxr_unilateral_opacities",
    "copd",
    "asthma",
    "hypertension",
    "diabetes",
    "pulmonary_dx",
    "heart_disease",
    "malignancy",
    "ckd",
    "hd",
    "immunocompromised",
    "hiv",
    "other_comorbidity_bool",
    "ace",
    "arb",
    "pronation_treatment",
    "glucose_6",
    "nsaid",
]

retrospective_categorical_columns = [
    "sex",
    "race",
    "residence",
    "admission_level",
    "discharge_destination_1",
    "discharge_destination_2",
    "g6pd-def1-norml0-inter2",
]

retrospective_numerical_columns = [
    "age",
    "bmi",
    "days_of_symptoms_before_1st_admission",
    "fever_duration",
    "initial_temp",
    "max_temp_admission",
    "systolic_bp",
    "diastolic_bp",
    "initial_rr",
    "o2_saturation",
    "composite",
    "chloroquine_days",
    "hydroxychloroquine_days",
    "kaletra_days",
    "remdesivir_compassionate_days",
    "remdesivir_clinical_trial_days",
    "pressors_days",
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

string_columns = [
    "other_symptoms",
    "lung_exam",
    "concurrent_pathogen_infection",
    "admission_xray",
    "cxr_interstitial",
    "initial_lung_ultrasound",
    "initial_heart_ultrasound",
    "other_comorbidity",
    "other_trial",
    "other_iv_abx",
    "glucocorticoids",
]

retrospective_feature_columns = [
    'wbcadmac',
    'wbcpeakac',
    'wbcnadirac',
    'crpeakac',
    'cradmac',
    'bunadmac',
    'neutadmac',
    'neutnadirac',
    'lymphadmac',
    'lymphnadirac',
    'pltpeakac',
    'pltnadirac',
    'pltadmac',
    'astpeakac',
    'astadmac',
    'altadmac',
    'ldhpeakac',
    'ldhadmac',
    'procalpeakac',
    'procaladmac',
    'crppeakac',
    'crpadmac',
    'ddimeradmac',
    'ddimerpeakac',
    'inradmac',
    'inrpeakac',
    'fibrinoadmac',
    'fibrinopeakac',
    'ferritadmac',
    'ferritpeakac',
    'pttadmac',
    'pttpeakac',
    'ptadmac',
    'ptpeakac',
    'alkpadmac',
    'alkppeakac',
    'albadmac',
    'il6initac',
    'il6peakac',
    'eosadmac',
    'g6pd-def1-norml0-inter2',
    'bpsystac',
    'bpdiastac',
    'tempinitac',
    'tempmaxac',
    'rrinitac',
    'pulseoxinitac',
    'readmission',
    'composite',
    'death',
    'dob',
    'age',
    'sex',
    'hispanic',
    'race',
    'residence',
    'hcw',
    'smoker',
    'bmi',
    'admission_level',
    'discharge_destination_1',
    'discharge_destination_2',
    'days_of_symptoms_before_1st_admission',
    'still_inpatient',
    'fever',
    'cough',
    'shortness_of_breath',
    'fatigue',
    'sore_throat',
    'chills',
    'headache',
    'diarrhea',
    'fever_duration',
    'initial_temp',
    'max_temp_admission',
    'systolic_bp',
    'diastolic_bp',
    'initial_rr',
    'o2_saturation',
    'altered_mental_status',
    'antipyretics',
    'received_oral_meds_in_1st_24hr',
    'on_o2_at_presentation',
    'intubation',
    'hi_flow',
    'non_rebreather_mask',
    'cpap_bpap',
    'nasal_cannula',
    'aki',
    'sepsis',
    'cardiogenic_shock',
    'myocarditis',
    'cardiac_arrest',
    'ards',
    'ecmo',
    'covid_result_1',
    'covid_result_2',
    'covid_result_3',
    'cxr_bilateral_opacities',
    'cxr_unilateral_opacities',
    'copd',
    'asthma',
    'hypertension',
    'diabetes',
    'pulmonary_dx',
    'heart_disease',
    'malignancy',
    'ckd',
    'hd',
    'immunocompromised',
    'hiv',
    'other_comorbidity_bool',
    'ace',
    'arb',
    'chloroquine_days',
    'hydroxychloroquine_days',
    'kaletra_days',
    'remdesivir_compassionate_days',
    'remdesivir_clinical_trial_days',
    'pressors_days',
    'pronation_treatment',
    'glucose_6',
    'nsaid',
    'a1c',
    'cd4_count_most_recent',
    'cd4_percent_most_recent',
    'concurrent_pathogen_infection_bool',
 ]

eap_boolean_columns = eap.binary_columns
eap_numerical_columns = eap.numerical_columns
eap_categorical_columns = eap.categorical_columns

def featurize_bool(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    """
    Maps boolean values in the column to [0,1] or [1,0] one-hot vectors.
    """
    true = one_hot(0, 2)
    false = one_hot(1,2)
    null = one_hot(None, 2)
    d2 = df.copy()
    for col in columns:
        d2[col] = d2[col].map({True: true, False: false, None: null, np.nan: null})
    return d2

def featurize_numeric(df: pd.DataFrame, columns: List[str]) -> Tuple[pd.DataFrame, pd.Series, pd.Series]:
    """
    Normalizes the numerical values in the column to have mean 0 and variance 1,
    and then returns the mean and variance.
    """
    mean = df[columns].mean()
    variance = df[columns].var()
    if len(mean) != len(columns):
        difference = [x for x in columns if x not in mean.index]
        raise ValueError("Could not convert to numeric the following columns: {0}.".format(", ".join(difference)))
    
    d2 = df.copy()
    d2[columns] = (d2[columns]-mean)/np.sqrt(variance)

    return d2, mean, variance

def featurize_categorical(df: pd.DataFrame, columns: List[str]) -> Tuple[pd.DataFrame, Dict]:
    """
    Converts the categorical values into one-hot vectors and returns a
    dictionary with those mappings.
    """
    d2 = df.copy()
    ids_dict = {}
    for col in columns:
        categories = set(df[col].dropna())
        if len(categories):
            ids = {category: i for category, i in zip(categories, count())}
            ids_dict[col] = ids
            d2[col] = d2[col].apply(lambda x: one_hot(ids.get(x), len(ids)))

    return d2, ids_dict

def one_hot(index: int, max_index: int) -> np.array:
    """
    Returns a one-hot vector corresponding to the given index with size =
    max_index.
    If index == None, then this will return a vector of zeros.
    """
    one = np.zeros(max_index)
    if index is not None:
        one[index] = 1
    
    return one

def featurize_dataset(df: pd.DataFrame, dataset: str) -> Tuple[pd.DataFrame, Dict, pd.Series, pd.Series]:
    """
    Featurizes all columns that can be and returns the new dataframe along with
    a dict containing the representations for each categorical column and then
    the means and variances of the numerical columns.
    """

    if dataset == 'retrospective':
        boolean_columns = retrospective_boolean_columns
        categorical_columns = retrospective_categorical_columns
        numerical_columns = retrospective_numerical_columns
    elif dataset == 'eap':
        boolean_columns = eap_boolean_columns
        categorical_columns = eap_categorical_columns
        numerical_columns = eap_numerical_columns

    else:
        raise ValueError(f"Dataset must be either 'retrospective' or 'eap', not {dataset}.")
    d2 = df.copy()
    d2 = featurize_bool(d2, boolean_columns)
    d2, category_dict = featurize_categorical(d2, categorical_columns)
    d2, mean, variance = featurize_numeric(d2, numerical_columns)

    return d2, category_dict, mean, variance

def interpolate_boolean(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    """
    Fills in missing boolean values with False.
    """
    d2 = df.copy()
    d2[columns] = d2[columns].fillna(False)
    
    return d2

def interpolate_numerical(df: pd.DataFrame, means: Dict[str,float]) -> pd.DataFrame:
    """
    Fills in missing numerical values with the mean using the key, value pairs
    in means.
    """
    d2 = df.copy()
    for col, mean in means.items():
        d2[col] = d2[col].fillna(mean)
    
    return d2

def interpolate_categorical(df: pd.DataFrame, categories: Dict[str, Dict[str, int]]) -> pd.DataFrame:
    """
    Fills in missing one-hot vectors for categorical data with a vector of all zeros.
    """
    d2 = df.copy()
    for col, table in categories.items():
        zeros = one_hot(None, len(table)).tolist()
        d2[col] = d2[col].fillna(zeros)
    
    return d2

def interpolate_dataset(df: pd.DataFrame, means: pd.Series, categories: Dict[str, Dict[str, int]]) -> pd.DataFrame:
    """
    Interpolates all columns in the dataset.
    """

    d2 = df.copy()
    #d2 = interpolate_boolean(d2, d2.columns.intersection(retrospective_boolean_columns))
    d2 = interpolate_numerical(d2, means.to_dict())
    #d2 = interpolate_categorical(d2, categories)

    return d2

def nonnullsubset(df: pd.DataFrame, features: List) -> pd.DataFrame:
    """
    Returns a subset of the input dataframe where the 
    """
def stack_dataset(df: pd.DataFrame, columns: pd.Index = None, categories_dict: Dict[str, Dict[str, int]] = None) -> Tuple[np.array, pd.Series]:
    """
    Stacks together all of the columns requested into a single matrix and
    returns a Series mapping column names to columns in the matrix.
    """

    labels = []
    columns = columns or df.columns
    numerical_cols = columns.intersection(retrospective_numerical_columns)
    boolean_cols = columns.intersection(retrospective_boolean_columns)
    categorical_cols = columns.intersection(retrospective_categorical_columns)

    array = None
    
    if len(numerical_cols):

        numerical_array = np.array(df[numerical_cols])
        labels.extend(numerical_cols)
        array = numerical_array

    if len(boolean_cols):
        bools = [np.stack(df[b]) for b in boolean_cols]
        for col in boolean_cols: # Account for true and false
            labels.extend([f"{col}=true", f"{col}=false"])

        bool_array = np.hstack(bools)
        if array is not None:
            array = np.hstack([array, bool_array])
        else:
            array = bool_array

    if len(categorical_cols):
        categoricals = [np.stack(df[c]) for c in categorical_cols]
        for col, categorical in zip(categorical_cols, categoricals):
            if categories_dict and col in categories_dict:
                sublabels = sorted(categories_dict[col], key=categories_dict[col].get)
                labels.extend([f"{col}={sublabel}" for sublabel in sublabels])
            else:
                labels.extend([col for _ in range(categorical.shape[1])])

        categorical_array = np.hstack(categoricals)
        bool_array = np.hstack(bools)
        if array is not None:
            array = np.hstack([array, categorical_array])
        else:
            array = categorical_array

    return array, pd.Series(labels)

from sklearn.base import BaseEstimator
class PredictThePrior(BaseEstimator):

    _estimator_type = "classifier"
    classes_ = [0,1]
    def fit(self, X, y):
        self.vec = [1-np.mean(y), np.mean(y)]

    def predict(self, X):
        return np.array([np.argmax(self.vec) for _ in range(len(X))])

    def predict_proba(self, X):

        return np.array([self.vec for _ in range(len(X))])