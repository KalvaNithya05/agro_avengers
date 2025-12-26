"""Inference script: load trained models and predict on a CSV.

Usage:
  python scripts/infer.py [input_csv]

Outputs `outputs/predictions.csv` with added columns `pred_crop` and `pred_yield` when models exist.
"""
import os
import sys
import joblib
import numpy as np
import pandas as pd

# Make project importable
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer


def transform_with_saved_preprocessor(df: pd.DataFrame, preprocessor_path: str):
    """Load a saved preprocessor and transform the input DataFrame.

    Returns transformed array on success, or raises if transform fails.
    """
    preproc = joblib.load(preprocessor_path)
    X = df.copy()

    # Determine expected input columns for the saved preprocessor
    expected_cols = None
    if hasattr(preproc, 'feature_names_in_'):
        expected_cols = list(preproc.feature_names_in_)
    else:
        # Try to extract column selectors from transformers_
        expected_cols = []
        try:
            for name, transformer, cols in preproc.transformers_:
                if cols is None or cols == 'drop' or cols == 'passthrough':
                    continue
                if isinstance(cols, (list, tuple, np.ndarray)):
                    expected_cols.extend(list(cols))
        except Exception:
            expected_cols = None

    # If we determined expected columns, ensure they exist in X (fill missing with NaN)
    if expected_cols:
        for c in expected_cols:
            if c not in X.columns:
                X[c] = np.nan

    # Transform using the saved preprocessor
    return preproc.transform(X)


def main():
    in_csv = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser(r"c:/Users/NITHYA/Downloads/mitti_mitra_master_dataset_all_india.csv")
    if not os.path.exists(in_csv):
        print('Input CSV not found:', in_csv)
        sys.exit(1)

    df = pd.read_csv(in_csv)
    outputs = df.copy()
    # Try classifier preprocessor first
    clf_preproc_path = os.path.join('models', 'preprocessor_clf.joblib')
    reg_preproc_path = os.path.join('models', 'preprocessor_reg.joblib')

    # Default placeholders
    clf_X = None
    reg_X = None

    if os.path.exists(clf_preproc_path):
        try:
            clf_X = transform_with_saved_preprocessor(df, clf_preproc_path)
            print('Transformed input with classifier preprocessor')
        except Exception as e:
            print('Failed to transform with classifier preprocessor:', e)

    if os.path.exists(reg_preproc_path):
        try:
            reg_X = transform_with_saved_preprocessor(df, reg_preproc_path)
            print('Transformed input with regressor preprocessor')
        except Exception as e:
            print('Failed to transform with regressor preprocessor:', e)

    # Fall back to simple_per-inference transform if needed
    if clf_X is None or reg_X is None:
        try:
            X_trans, feat_names = simple_preprocess_for_inference(df)
            if clf_X is None:
                clf_X = X_trans
            if reg_X is None:
                reg_X = X_trans
            print('Used simple inference preprocessor fallback')
        except Exception as e:
            print('Fallback preprocessing failed:', e)
            clf_X = clf_X or None
            reg_X = reg_X or None
    os.makedirs('outputs', exist_ok=True)

    # Classifier
    clf_path = os.path.join('models', 'rf_crop_model.joblib')
    if os.path.exists(clf_path):
        clf = joblib.load(clf_path)
        try:
            if clf_X is None:
                raise RuntimeError('No preprocessed input available for classifier')
            preds = clf.predict(clf_X)
            outputs['pred_crop'] = preds
            print('Classifier predictions added.')
        except Exception as e:
            print('Classifier predict failed:', e)
    else:
        print('Classifier model not found at', clf_path)

    # Regressor
    reg_path = os.path.join('models', 'xgb_yield_model.joblib')
    if os.path.exists(reg_path):
        reg = joblib.load(reg_path)
        try:
            if reg_X is None:
                raise RuntimeError('No preprocessed input available for regressor')
            preds = reg.predict(reg_X)
            outputs['pred_yield'] = preds
            print('Regressor predictions added.')
        except Exception as e:
            print('Regressor predict failed:', e)
    else:
        print('Regressor model not found at', reg_path)

    out_file = os.path.join('outputs', 'predictions.csv')
    outputs.to_csv(out_file, index=False)
    print('Saved predictions to', out_file)


if __name__ == '__main__':
    main()
