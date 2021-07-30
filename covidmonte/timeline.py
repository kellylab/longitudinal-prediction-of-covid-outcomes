import pandas as pd
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def plot_timeline(s: pd.Series, ax):

    data = [(x,col) for x,col in zip(s,s.index) if isinstance(x,datetime) and x is not pd.NaT]
    events = [x[1] for x in data]
    dates = [x[0] for x in data]
    
    levels = np.tile([-11, 11, -9, 9, -7, 7, -5, 5, -3, 3, -1, 1], int(np.ceil(len(dates)/12)))[:len(dates)]

    # Create figure and plot a stem plot with the date
    patient_id = s.index
    ax.set(title=f"Event History for Patient {patient_id}")

    markerline, stemline, baseline = ax.stem(dates, levels,
                                            linefmt="C3-", basefmt="k-",
                                            use_line_collection=True)

    plt.setp(markerline, mec="k", mfc="w", zorder=3)

    # Shift the markers to the baseline by replacing the y-data by zeros.
    markerline.set_ydata(np.zeros(len(dates)))

    # annotate lines
    vert = np.array(['top', 'bottom'])[(levels > 0).astype(int)]
    for d, l, r, va in zip(dates, levels, events, vert):
        ax.annotate(r, xy=(d, l), xytext=(-3, np.sign(l)*3),
                    textcoords="offset points", va=va, ha="right")

    # format xaxis with daily intervals
    ax.get_xaxis().set_major_locator(mdates.DayLocator(interval=1))
    ax.get_xaxis().set_major_formatter(mdates.DateFormatter("%d %b %Y"))
    plt.setp(ax.get_xticklabels(), rotation=30, ha="right")

    # remove y axis and spines
    ax.get_yaxis().set_visible(False)
    for spine in ["left", "top", "right"]:
        ax.spines[spine].set_visible(False)

    ax.margins(y=0.1)
    
    return ax