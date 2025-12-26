"""Train crop recommendation and yield prediction models using the provided pan-India dataset.

Usage:
  python scripts/train_models.py

The script looks for the dataset at the Downloads path used when you attached
the file. If not found there it will try `data/` inside the repo.

Outputs:
- Saved models in `models/` (joblib)
- Printed evaluation metrics and feature importances
"""
import os
import sys
import joblib

# Ensure project root is importable when running scripts from workspace root
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
import traceback
from pathlib import Path

import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, mean_squared_error, r2_score

try:
    from xgboost import XGBRegressor
except Exception:
    XGBRegressor = None

from ml.preprocess import load_dataset, identify_targets, preprocess_features


DATA_PATHS = [
    os.path.join(os.getcwd(), 'data', 'mitti_mitra_master_dataset_all_india.csv'),
    os.path.expanduser(r"c:/Users/NITHYA/Downloads/mitti_mitra_master_dataset_all_india.csv"),
]


def find_dataset() -> str:
    for p in DATA_PATHS:
        if os.path.exists(p):
            return p
    raise FileNotFoundError(f"Dataset not found. Checked: {DATA_PATHS}")


def train_classification(X, y, feature_names=None):
    print("Training RandomForestClassifier for crop recommendation...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    param_grid = {
        'n_estimators': [100, 200],
        'max_depth': [10, 20, None]
    }
    clf = RandomForestClassifier(random_state=42)
    gs = GridSearchCV(clf, param_grid, cv=3, scoring='f1_macro', n_jobs=-1)
    gs.fit(X_train, y_train)

    best = gs.best_estimator_
    y_pred = best.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, average='macro')

    print(f"Best params: {gs.best_params_}")
    print(f"Accuracy: {acc:.4f}")
    print(f"F1 (macro): {f1:.4f}")

    # Feature importance
    try:
        importances = best.feature_importances_
        if feature_names is not None and len(feature_names) == len(importances):
            fi = sorted(zip(feature_names, importances), key=lambda x: -x[1])[:20]
            print("Top feature importances (classification):")
            for name, val in fi:
                print(f"  {name}: {val:.4f}")
    except Exception:
        print("Could not extract feature importances for classifier")

    # Save model
    os.makedirs('models', exist_ok=True)
    joblib.dump(best, 'models/rf_crop_model.joblib')
    print('Saved classifier to models/rf_crop_model.joblib')


def train_regression(X, y, feature_names=None):
    print("Training XGBoostRegressor for yield prediction...")
    if XGBRegressor is None:
        print("XGBoost not available. Skipping regression training.")
        return

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    param_grid = {
        'n_estimators': [100, 200],
        'learning_rate': [0.1, 0.01],
        'max_depth': [3, 6]
    }
    reg = XGBRegressor(random_state=42, objective='reg:squarederror')
    gs = GridSearchCV(reg, param_grid, cv=3, scoring='neg_root_mean_squared_error', n_jobs=-1)
    gs.fit(X_train, y_train)

    best = gs.best_estimator_
    y_pred = best.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)

    print(f"Best params: {gs.best_params_}")
    print(f"RMSE: {rmse:.4f}")
    print(f"R2: {r2:.4f}")

    # Feature importance
    try:
        importances = best.feature_importances_
        if feature_names is not None and len(feature_names) == len(importances):
            fi = sorted(zip(feature_names, importances), key=lambda x: -x[1])[:20]
            print("Top feature importances (regression):")
            for name, val in fi:
                print(f"  {name}: {val:.4f}")
    except Exception:
        print("Could not extract feature importances for regressor")

    os.makedirs('models', exist_ok=True)
    joblib.dump(best, 'models/xgb_yield_model.joblib')
    print('Saved regressor to models/xgb_yield_model.joblib')


def main():
    try:
        path = find_dataset()
        print('Using dataset:', path)
        df = load_dataset(path)
        print('Dataset shape:', df.shape)

        clf_target, reg_target = identify_targets(df)
        print('Detected classification target:', clf_target)
        print('Detected regression target:', reg_target)

        # Train classifier if target found
        if clf_target:
            Xc, yc, preproc_c, feat_names_c = preprocess_features(df, clf_target)
            # Save preprocessor and feature names for inference
            os.makedirs('models', exist_ok=True)
            try:
                joblib.dump(preproc_c, 'models/preprocessor_clf.joblib')
                joblib.dump(feat_names_c, 'models/feature_names_clf.joblib')
                print('Saved classifier preprocessor and feature names')
            except Exception:
                print('Warning: failed to save classifier preprocessor')

            train_classification(Xc, yc, feat_names_c)
        else:
            print('No classification target detected; skipping classifier training')

        # Train regressor if target found
        if reg_target:
            Xr, yr, preproc_r, feat_names_r = preprocess_features(df, reg_target)
            try:
                joblib.dump(preproc_r, 'models/preprocessor_reg.joblib')
                joblib.dump(feat_names_r, 'models/feature_names_reg.joblib')
                print('Saved regressor preprocessor and feature names')
            except Exception:
                print('Warning: failed to save regressor preprocessor')

            train_regression(Xr, yr, feat_names_r)
        else:
            print('No regression target detected; skipping regression training')

    except Exception:
        print('Training pipeline failed:')
        traceback.print_exc()


if __name__ == '__main__':
    main()
