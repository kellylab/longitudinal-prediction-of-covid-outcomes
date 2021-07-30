import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from typing import List, Tuple
import numpy as np

def precision_recall(precision: List[np.array], recall: List[np.array], ax: plt.Axes, label=None) -> plt.Axes:
    """
    Interpolates and plots as a heatmap the precision-recall values. This does
    not plot a single precision-recall curve but rather takes a listing of
    precision and recall values and plots them all together as a density. This
    is useful for visualizing the variability in prc over multiple iterations.
    """
    z = np.linspace(0,1,100)
    if len(precision) != len(recall):
        raise ValueError("Precision and recall lists must be the same length.")
    y = []
    for prec, rec in zip(precision, recall):
        prec = np.insert(prec, [-1], [0,1])
        rec = np.insert(rec, [-1], [1,0])
        f = interp1d(rec, prec)
        y.append(f(z))

    y = np.array(y)
    var = np.var(y, 0)
    interval_sizes = var # / np.sqrt(len(precision)-1)
    means = np.mean(y,0)
    auc = np.trapz(means, z)
    ax.errorbar(z,means,yerr=interval_sizes / np.sqrt(len(precision)-1))
    if label:
        label = f"{label} (Mean AUC={auc})"
    else:
        label = f"Mean AUC={auc}"
    ax.fill_between(z,means-interval_sizes, means+interval_sizes, alpha=.3, label=label)
    #ax.plot(z, means, 'k-', label=f"Mean AUC={auc}")
    return ax

def roc(tprs: List[np.array], fprs: List[np.array], ax: plt.Axes, label=None) -> plt.Axes:
    """
    Interpolates and plots as a heatmap the precision-recall values. This does
    not plot a single precision-recall curve but rather takes a listing of
    precision and recall values and plots them all together as a density. This
    is useful for visualizing the variability in prc over multiple iterations.
    """
    z = np.linspace(0,1,100)
    if len(tprs) != len(fprs):
        raise ValueError("Precision and recall lists must be the same length.")
    y = []
    for tpr, fpr in zip(tprs, fprs):
        tpr = np.insert(tpr, [-1], [1,0])
        fpr = np.insert(fpr, [-1], [1,0])
        f = interp1d(fpr, tpr)
        y.append(f(z))

    y = np.array(y)
    var = np.var(y, 0)
    interval_sizes = var #/ np.sqrt(len(precision)-1)
    means = np.mean(y,0)
    auc = np.trapz(means, z)
    ax.errorbar(z,means,yerr=interval_sizes / np.sqrt(len(tprs)-1))
    if label:
        label = f"{label} (Mean AUC={auc})"
    else:
        label = f"Mean AUC={auc}"
    ax.fill_between(z,means-interval_sizes, means+interval_sizes, alpha=.3, label=label)
    #ax.plot(z, means, 'k-', label=f"Mean AUC={auc}")

    return ax