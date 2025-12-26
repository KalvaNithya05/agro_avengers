import os
import joblib
import pandas as pd
import numpy as np

BASE = os.path.dirname(os.path.dirname(__file__))
MODEL_DIR = os.path.join(BASE, 'models')

def load(path):
    p = os.path.join(BASE, path)
    if not os.path.exists(p):
        raise FileNotFoundError(p)
    return joblib.load(p)


def main():
    try:
        preproc_clf = load('models/preprocessor_clf.joblib')
        preproc_reg = load('models/preprocessor_reg.joblib')
        rf = load('models/rf_crop_model.joblib')
        xgb = load('models/xgb_yield_model.joblib')
    except Exception as e:
        print('Model load error:', e)
        return

    # Sample input — adapt keys to common columns seen in dataset
    sample = {
        'soil_n': 200,
        'soil_p': 50,
        'soil_k': 80,
        'soil_ph': 6.5,
        'avg_temperature': 27.0,
        'avg_rainfall': 120.0,
        'humidity': 60.0,
        'state': 'Karnataka',
        'season': 'Kharif',
        'crop_type': 'Cereals'
    }

    df = pd.DataFrame([sample])

    # Ensure columns expected by preprocessor are present
    expected = []
    if hasattr(preproc_clf, 'feature_names_in_'):
        expected = list(preproc_clf.feature_names_in_)
    elif hasattr(preproc_clf, 'transformers_'):
        # best-effort: combine numeric and categorical names if available
        try:
            expected = list(preproc_clf.transformers_[0][2]) + list(preproc_clf.transformers_[1][2])
        except Exception:
            expected = []

    for c in expected:
        if c not in df.columns:
            df[c] = np.nan

    print('Input columns prepared:', df.columns.tolist())

    try:
        Xc = preproc_clf.transform(df)
        probs = rf.predict_proba(Xc)
        classes = rf.classes_
        top = np.argsort(probs[0])[::-1][:3]
        print('Top crop predictions:')
        for i in top:
            print(classes[i], float(probs[0][i]))
    except Exception as e:
        print('Classifier inference failed:', e)

    try:
        # If regression depends on crop, set crop to top predicted class if available
        try:
            top_crop = classes[top[0]]
            if 'crop' not in df.columns:
                df['crop'] = top_crop
        except Exception:
            pass
        Xr = preproc_reg.transform(df)
        ypred = xgb.predict(Xr)
        print('Predicted yield:', float(ypred[0]))
    except Exception as e:
        print('Regressor inference failed:', e)


if __name__ == '__main__':
    main()
