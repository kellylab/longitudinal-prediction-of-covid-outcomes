import pandas as pd
import math
from typing import Dict
import numpy as np

def strip_spaces_from_columns(df):
    """
    Removes trailing spaces from column names.
    """
    d2 = df.copy()
    for col in d2.columns:
        d2 =d2.rename(columns={col: col.strip()})
    
    return d2

def true_false(h):
    """
    Converts boolean columns, returning None when value is not specified.
    """
    
    bool_dict = {
        '0': False,
        '1': True,
        0: False,
        1: True,
        0.: False,
        1.: True,
        "Yes": True,
        "No": False,
    }
    if h in bool_dict:
        return bool_dict[h]
    elif type(h) is str and len(h)>2:
        return True
    else:
        return None

def coerce_type(x, t):
    """
    Coerces x to have type t, returning None on failure.
    """
    try:
        return t(x)
    except:
        return

def str2bool(s):
    """
    Useful for booleanizing columns where there can be some text describing the
    entry and a 0 if nothing is present (eg. the type of bacterial infection).
    """
    if type(s) is float and math.isnan(s):
        return np.nan
    return bool(s)

def rename(df: pd.DataFrame, renaming_dict: Dict[str,str]) -> pd.DataFrame:
    """
    Renames df based on old:new pairs in renaming_dict
    """
    for old_name, new_name in renaming_dict.items():
        df[new_name] = df[old_name]

    to_drop = [k for k,v in renaming_dict.items() if k!=v]

    df = df.drop(columns=list(to_drop))

    return df
