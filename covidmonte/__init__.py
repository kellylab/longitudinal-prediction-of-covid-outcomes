import pandas as pd
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import logging
import sys

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class Plotter():
    """
    Context manager which creates, saves, and shows a plot on exit.
    """
    def __init__(self, filename, *args, show=True, **kwargs):

        self.filename = filename
        self.args = args
        self.kwargs = kwargs
        self.show = show

    def __enter__(self):
        self.fig, self.ax = plt.subplots(*self.args, **self.kwargs)
        return self.ax

    def __exit__(self, exc_type, exc_val, traceback):
        if exc_type is not None:
            # Pass through errors
            raise exc_type(str(exc_val))
        self.fig.savefig(self.filename)
        if self.show:
            plt.show(self.fig)

        plt.close(self.fig)
        return True

def get_retrospective_data(regenerate:bool=False, study=None) -> pd.DataFrame:
    """
    Loads the data in from pickle or generates it.
    """

    if not regenerate:
        try:
            df = pd.read_pickle("data/confidential/retrospective.pickle")
        except FileNotFoundError:            
            logger.warning("Could not find processed patient data, so creating the file now...")
    else:
        logger.info("Regenerating processed dataset...")

        from covidmonte.clean_retrospective import clean_data
        try:
            df = pd.read_excel("data/raw/COVID19_RETROSPECTIVE_DATA.5.15.xlsx")
        except:
            logger.critical("Could not find raw data in data/raw/COVID19_RETROSPECTIVE_DATA.5.15.xlsx. Please make sure you have it.")
            sys.exit()
        df = clean_data(df)
        df.to_pickle("data/confidential/retrospective.pickle")
        df.to_csv("data/confidential/retrospective.csv")
        df.to_hdf("data/confidential/retrospective.hdf", key="covid")

    if study:
        return filter_study(df, study)
    else:
        return df

def get_eap_data(regenerate=False):

    #df = pd.read_csv("data/confidential/0523eap_data.csv")

    if not regenerate:
        try:
            df = pd.read_csv("data/confidential/eap.csv")
            return df
        except IOError:
            logger.warning("Could not find processed EAP data, so creating the file now...")

    logger.info("Regenerating EAP data...")
    codex = pd.read_csv("data/processed/eap_file_keys.csv")
    codex = {row['label_raw']: row['label_new'] for _, row in codex.iterrows()}
    from .clean_eap import clean_eap
    df = clean_eap(df, codex)
    df.to_csv("data/confidential/eap.csv")

    return df

def filter_study(df: pd.DataFrame, study: str) -> pd.DataFrame:
    """
    Returns the rows of the df which match the given study. Some patients are in
    multiple studies, so this is not a 1:1 mapping.
    """
    if study not in studies:
        raise ValueError(f"Study {study} does not exist in the dataset.")

    which_ones = df['study_member'].apply(lambda x: True if study in str(x) else False)

    return df[which_ones]
