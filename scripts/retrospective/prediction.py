from covidmonte import *
from covidmonte.retrospective import *
from covidmonte.ml import *
import seaborn as sns
import os
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import plot_roc_curve, plot_precision_recall_curve, average_precision_score, roc_auc_score
from sklearn.multiclass import OneVsRestClassifier
import pandas as pd
import multiprocessing
base_path = "data/plots/retrospective/prediction"

df = get_retrospective_data()

outcomes_columns = [
    'death', 'intubation', 'non_rebreather_mask', 'cpap_bpap', 'nasal_cannula',
    'ecmo',
    ]

vectorized, categorical_dict, means, variances = featurize_dataset(df)
interpolated = interpolate_dataset(vectorized, means, categorical_dict)
interpolated = interpolated[numerical_columns]
interpolated = interpolated.T.drop_duplicates().T
data, columns = stack_dataset(interpolated, categories_dict=categorical_dict)
filled = pd.DataFrame(data, columns=columns)
to_drop = filled.columns[filled.isna().any()]
if len(to_drop):
    filled = filled.drop(columns=to_drop)
    columns = [x for x in columns if x not in to_drop]
data = np.array(filled)

ml_df = df[0:750]
outcomes = ml_df[outcomes_columns].fillna(0.).astype(int)
everything_else = ml_df[ml_df.columns.difference(outcomes_columns).difference(date_columns).difference(['qsofa', 'qsofarr', 'composite'])]
predictor = np.array(everything_else.isna().astype(int))
label = np.array(outcomes)


for i, col in enumerate(outcomes_columns):
    with Plotter(os.path.join(base_path, f"missing_data_aupr_{col}.svg"), figsize=(15,15), show=False) as ax:
        def func(n):
            X_train, X_test, y_train, y_test = train_test_split(predictor, label)
            clf = OneVsRestClassifier(RandomForestClassifier())
            clf.fit(X_train, y_train)
            predictions = clf.predict(X_test)
            average_precision = average_precision_score(y_test[:,i], predictions[:,i])
            plot_precision_recall_curve(clf.estimators_[i],X_test,y_test[:,i], ax=ax, label="AP={0:.02f}".format(average_precision))
        pool = multiprocessing.Pool(processes=12)
        pool.map(func, range(10))
        ax.set_title(f"Precision-Recall for Missing Data vs. {col}")
        ax.legend()


for i, col in enumerate(outcomes_columns):
    features = []
    with Plotter(os.path.join(base_path, f"missing_data_roc_{col}.svg"), figsize=(15,15), show=False) as ax:
        for _ in range(10): # Make 10 runs
            X_train, X_test, y_train, y_test = train_test_split(predictor, label)
            clf = OneVsRestClassifier(RandomForestClassifier())
            clf.fit(X_train, y_train)
            predictions = clf.predict(X_test)
            try:
                auc = roc_auc_score(y_test[:,i], predictions[:,i])
                plot_roc_curve(clf.estimators_[i],X_test,y_test[:,i], ax=ax, label="AUC={0:.02f}".format(auc))
            except ValueError:
                pass
            features.append(pd.DataFrame({"score": clf.estimators_[i].feature_importances_}, index=everything_else.columns).sort_values("score", ascending=False))
        ax.set_title(f"ROC for Missing Data vs. {col}")
        ax.legend()
    with Plotter(os.path.join(base_path, f"missing_data_features_{col}.svg"), figsize=(15,15), show=False) as ax:
        features = pd.concat(features,axis=1).T
        features[features.columns[features.mean() > .005]].plot.box(vert=False, ax=ax, fontsize=14)
        ax.set_title(f"Feature Importance Scores for Missing Data vs. {col}.")

labs_columns.remove("g6pd-def1-norml0-inter2")
labs_columns = list(set(labs_columns))
# Now do it for labs
everything_else = ml_df[labs_columns]
predictor = np.array(everything_else.isna().astype(int))
label = np.array(outcomes)

for i, col in enumerate(outcomes_columns):
    with Plotter(os.path.join(base_path,"labs", f"missing_labs_aupr_{col}.svg"), figsize=(15,15), show=False) as ax:
        for _ in range(10): # Make 10 runs
            X_train, X_test, y_train, y_test = train_test_split(predictor, label)
            clf = OneVsRestClassifier(RandomForestClassifier())
            clf.fit(X_train, y_train)
            predictions = clf.predict(X_test)
            average_precision = average_precision_score(y_test[:,i], predictions[:,i])
            plot_precision_recall_curve(clf.estimators_[i],X_test,y_test[:,i], ax=ax, label="AP={0:.02f}".format(average_precision))
        ax.set_title(f"Precision-Recall for Missing Labs vs. {col}")
        ax.legend()


for i, col in enumerate(outcomes_columns):
    features = []
    with Plotter(os.path.join(base_path, "labs", f"missing_labs_roc_{col}.svg"), figsize=(15,15), show=False) as ax:
        for _ in range(10): # Make 10 runs
            X_train, X_test, y_train, y_test = train_test_split(predictor, label)
            clf = OneVsRestClassifier(RandomForestClassifier())
            clf.fit(X_train, y_train)
            predictions = clf.predict(X_test)
            try:
                auc = roc_auc_score(y_test[:,i], predictions[:,i])
                plot_roc_curve(clf.estimators_[i],X_test,y_test[:,i], ax=ax, label="AUC={0:.02f}".format(auc))
            except ValueError:
                pass
            try:
                features.append(pd.DataFrame({"score": clf.estimators_[i].feature_importances_}, index=everything_else.columns).sort_values("score", ascending=False))
            except AttributeError:
                pass
        ax.set_title(f"ROC for Missing Labs vs. {col}")
        ax.legend()
    with Plotter(os.path.join(base_path, "labs", f"missing_labs_features_{col}.svg"), figsize=(15,15), show=False) as ax:
        features = pd.concat(features,axis=1).T
        features[features.columns[features.mean() > .005]].plot.box(vert=False, ax=ax, fontsize=14)
        ax.set_title(f"Feature Importance Scores for Missing Labs vs. {col}.")

# Now do it for actual labs values
everything_else = ml_df[labs_columns].fillna(ml_df[labs_columns].mean())
predictor = np.array(everything_else).astype(float)
label = np.array(outcomes)

for i, col in enumerate(outcomes_columns):
    with Plotter(os.path.join(base_path,"labs_values", f"labs_aupr_{col}.svg"), figsize=(15,15), show=False) as ax:
        for _ in range(10): # Make 10 runs
            X_train, X_test, y_train, y_test = train_test_split(predictor, label)
            clf = OneVsRestClassifier(RandomForestClassifier())
            clf.fit(X_train, y_train)
            predictions = clf.predict(X_test)
            average_precision = average_precision_score(y_test[:,i], predictions[:,i])
            plot_precision_recall_curve(clf.estimators_[i],X_test,y_test[:,i], ax=ax, label="AP={0:.02f}".format(average_precision))
        ax.set_title(f"Precision-Recall for Lab Values vs. {col}")
        ax.legend()


for i, col in enumerate(outcomes_columns):
    features = []
    with Plotter(os.path.join(base_path, "labs_values", f"labs_roc_{col}.svg"), figsize=(15,15), show=False) as ax:
        for _ in range(10): # Make 10 runs
            X_train, X_test, y_train, y_test = train_test_split(predictor, label)
            clf = OneVsRestClassifier(RandomForestClassifier())
            clf.fit(X_train, y_train)
            predictions = clf.predict(X_test)
            try:
                auc = roc_auc_score(y_test[:,i], predictions[:,i])
                plot_roc_curve(clf.estimators_[i],X_test,y_test[:,i], ax=ax, label="AUC={0:.02f}".format(auc))
            except ValueError:
                pass
            try:
                features.append(pd.DataFrame({"score": clf.estimators_[i].feature_importances_}, index=everything_else.columns).sort_values("score", ascending=False))
            except AttributeError:
                pass
        ax.set_title(f"ROC for Labs vs. {col}")
        ax.legend()
    with Plotter(os.path.join(base_path, "labs_values", f"labs_features_{col}.svg"), figsize=(15,15), show=False) as ax:
        features = pd.concat(features,axis=1).T
        features[features.columns[features.mean() > .005]].plot.box(vert=False, ax=ax, fontsize=14)
        ax.set_title(f"Feature Importance Scores for Labs vs. {col}.")