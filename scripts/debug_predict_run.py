import traceback
import pandas as pd
import numpy as np

from backend.api import predict as p
from backend.services.fertilizer_service import recommend_fertilizer

print('Loading models...')
try:
    p.load_models()
    print('Loaded: preproc_clf=', type(p.preproc_clf), 'rf_model=', type(p.rf_model))
    print('Loaded: preproc_reg=', type(p.preproc_reg), 'reg_model=', type(p.reg_model))
except Exception:
    traceback.print_exc()

# sample input
data = {'N':30,'P':35,'K':25,'ph':6.5,'temperature':28,'humidity':65,'rainfall':900,'state':'Telangana','season':'Kharif','crop_type':'Agriculture'}

# build input_row same as API
input_row = {}
input_row['soil_n'] = data.get('soil_n') or data.get('N')
input_row['soil_p'] = data.get('soil_p') or data.get('P')
input_row['soil_k'] = data.get('soil_k') or data.get('K')
input_row['soil_ph'] = data.get('soil_ph') or data.get('ph')
input_row['avg_temperature'] = data.get('avg_temperature') or data.get('temperature')
input_row['avg_rainfall'] = data.get('avg_rainfall') or data.get('rainfall')
input_row['humidity'] = data.get('humidity')
for k in ['state', 'district', 'agro_climatic_zone', 'season', 'crop_type']:
    if k in data:
        input_row[k] = data.get(k)

print('\nInput row:', input_row)

# classification
try:
    if p.preproc_clf is not None and p.rf_model is not None:
        df = pd.DataFrame([input_row])
        print('\nDF columns before:', df.columns.tolist())
        if hasattr(p.preproc_clf, 'feature_names_in_'):
            print('preproc_clf.feature_names_in_ length=', len(p.preproc_clf.feature_names_in_))
            for c in p.preproc_clf.feature_names_in_:
                if c not in df.columns:
                    df[c] = np.nan
        print('DF columns after:', df.columns.tolist())
        Xc = p.preproc_clf.transform(df)
        print('Xc shape:', getattr(Xc, 'shape', type(Xc)))
        probs = p.rf_model.predict_proba(Xc)
        classes = p.rf_model.classes_
        print('Probs dtype:', type(probs), 'classes dtype:', type(classes), 'classes example:', classes[:5])
        top_idx = np.argsort(probs[0])[::-1][:3]
        clf_preds = [
            {'crop': str(classes[i]), 'probability': float(probs[0][i])}
            for i in top_idx
        ]
        print('clf_preds:', clf_preds)
    else:
        print('Classifier or preprocessor missing')
except Exception:
    print('\nClassifier block exception:')
    traceback.print_exc()

# regression
try:
    if 'clf_preds' in locals() and clf_preds and p.preproc_reg is not None and p.reg_model is not None:
        yields = []
        for entry in clf_preds:
            dfr = pd.DataFrame([input_row])
            dfr['crop'] = entry['crop']
            if hasattr(p.preproc_reg, 'feature_names_in_'):
                for c in p.preproc_reg.feature_names_in_:
                    if c not in dfr.columns:
                        dfr[c] = np.nan
            Xr = p.preproc_reg.transform(dfr)
            val = float(p.reg_model.predict(Xr)[0])
            entry['predicted_yield'] = val
            yields.append(val)
        print('\nRegression yields:', yields)
    else:
        print('\nRegressor or preprocessor missing or no clf_preds')
except Exception:
    print('\nRegressor block exception:')
    traceback.print_exc()

# fertilizer
try:
    fert = recommend_fertilizer(input_row.get('soil_n'), input_row.get('soil_p'), input_row.get('soil_k'))
    print('\nFertilizer recommendations:', fert)
except Exception:
    print('\nFertilizer block exception:')
    traceback.print_exc()

# Attempt to JSON-serialize final response to mimic Flask jsonify
try:
    import json
    response_obj = {
        'status': 'success',
        'crops': clf_preds if 'clf_preds' in locals() else [],
        'predicted_yield': yields if 'yields' in locals() else None,
        'fertilizer_recommendations': fert,
        'used_params': data
    }
    s = json.dumps(response_obj)
    print('\nJSON serialization succeeded, length=', len(s))
except Exception:
    print('\nJSON serialization failed:')
    traceback.print_exc()
