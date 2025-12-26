from flask import Blueprint, request, jsonify
import os
import joblib
import numpy as np
import pandas as pd
from config.supabase_client import supabase
from services.fertilizer_service import recommend_fertilizer

predict_bp = Blueprint('predict', __name__)

# Paths
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
MODEL_DIR = os.path.join(REPO_ROOT, 'models')
RF_MODEL_PATH = os.path.join(MODEL_DIR, 'rf_crop_model.joblib')
XGB_MODEL_PATH = os.path.join(MODEL_DIR, 'xgb_yield_model.joblib')
PREPROC_CLF = os.path.join(MODEL_DIR, 'preprocessor_clf.joblib')
PREPROC_REG = os.path.join(MODEL_DIR, 'preprocessor_reg.joblib')

# Lazy-loaded objects
rf_model = None
reg_model = None
preproc_clf = None
preproc_reg = None


def load_models():
    """Load models and preprocessors lazily."""
    global rf_model, reg_model, preproc_clf, preproc_reg
    if rf_model is not None:
        return

    try:
        if os.path.exists(PREPROC_CLF):
            preproc_clf = joblib.load(PREPROC_CLF)
    except Exception as e:
        print('Could not load preprocessor_clf:', e)

    try:
        if os.path.exists(PREPROC_REG):
            preproc_reg = joblib.load(PREPROC_REG)
    except Exception as e:
        print('Could not load preprocessor_reg:', e)

    try:
        if os.path.exists(RF_MODEL_PATH):
            rf_model = joblib.load(RF_MODEL_PATH)
    except Exception as e:
        print('Could not load rf model:', e)

    try:
        if os.path.exists(XGB_MODEL_PATH):
            reg_model = joblib.load(XGB_MODEL_PATH)
    except Exception as e:
        print('Could not load regressor model:', e)


def enrich_with_zone(state: str):
    """Fetch agro_climatic_zone for a given state."""
    if not state or supabase is None:
        return None
    try:
        resp = supabase.table('mitti_mitra_data') \
            .select('agro_climatic_zone') \
            .eq('state', state) \
            .limit(1) \
            .execute()
        if getattr(resp, 'data', None):
            return resp.data[0].get('agro_climatic_zone')
    except Exception:
        pass
    return None


@predict_bp.route('/recommend', methods=['POST'])
def recommend():
    """
    Crop + Yield + Fertilizer recommendation API

    Expected JSON fields:
    N, P, K, ph, temperature, humidity, rainfall,
    state, season, crop_type
    """
    try:
        data = request.json or {}

        # Enrich agro-climatic zone
        if 'state' in data and 'agro_climatic_zone' not in data:
            zone = enrich_with_zone(data.get('state'))
            if zone:
                data['agro_climatic_zone'] = zone

        # Build input row for ML
        input_row = {}

        # Numeric inputs
        input_row['soil_n'] = data.get('soil_n') or data.get('N')
        input_row['soil_p'] = data.get('soil_p') or data.get('P')
        input_row['soil_k'] = data.get('soil_k') or data.get('K')
        input_row['soil_ph'] = data.get('soil_ph') or data.get('ph')
        input_row['avg_temperature'] = data.get('avg_temperature') or data.get('temperature')
        input_row['avg_rainfall'] = data.get('avg_rainfall') or data.get('rainfall')
        input_row['humidity'] = data.get('humidity')

        # Categorical inputs
        for k in ['state', 'district', 'agro_climatic_zone', 'season', 'crop_type']:
            if k in data:
                input_row[k] = data.get(k)

        clf_preds = []
        reg_preds = None

        # Load ML models
        load_models()

        # -------- Crop Classification --------
        if preproc_clf is not None and rf_model is not None:
            try:
                df = pd.DataFrame([input_row])
                if hasattr(preproc_clf, 'feature_names_in_'):
                    for c in preproc_clf.feature_names_in_:
                        if c not in df.columns:
                            df[c] = np.nan

                Xc = preproc_clf.transform(df)
                probs = rf_model.predict_proba(Xc)
                classes = rf_model.classes_

                top_idx = np.argsort(probs[0])[::-1][:3]
                clf_preds = [
                    {'crop': str(classes[i]), 'probability': float(probs[0][i])}
                    for i in top_idx
                ]
            except Exception as e:
                print('Classifier inference error:', e)

        # -------- Yield Prediction --------
        try:
            if clf_preds and preproc_reg is not None and reg_model is not None:
                yields = []
                for entry in clf_preds:
                    dfr = pd.DataFrame([input_row])
                    dfr['crop'] = entry['crop']

                    if hasattr(preproc_reg, 'feature_names_in_'):
                        for c in preproc_reg.feature_names_in_:
                            if c not in dfr.columns:
                                dfr[c] = np.nan

                    Xr = preproc_reg.transform(dfr)
                    val = float(reg_model.predict(Xr)[0])
                    entry['predicted_yield'] = val
                    yields.append(val)

                reg_preds = yields
        except Exception as e:
            print('Regressor inference error:', e)

        # -------- Fertilizer Recommendation (FIXED) --------
        soil_n = data.get('soil_n') or data.get('N')
        soil_p = data.get('soil_p') or data.get('P')
        soil_k = data.get('soil_k') or data.get('K')

        fertilizer_recommendations = recommend_fertilizer(
            soil_n=soil_n,
            soil_p=soil_p,
            soil_k=soil_k
        )

        # -------- Final Response --------
        return jsonify({
            'status': 'success',
            'crops': clf_preds,
            'predicted_yield': reg_preds,
            'fertilizer_recommendations': fertilizer_recommendations,
            'used_params': data
        })

    except Exception as e:
        print('Prediction API Error:', e)
        return jsonify({'error': 'Internal Server Error'}), 500
