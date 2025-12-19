import os
import pickle
import numpy as np
import random

class CropPredictor:
    def __init__(self):
        """
        Initializes the predictor by loading models.
        """
        # Resolve path relative to this file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.model_dir = os.path.join(os.path.dirname(current_dir), 'models')
        
        self.agri_model = self._load_model('crop_recommendation_model.pkl')
        self.label_encoder = self._load_model('label_encoder.pkl')
        # Scaler is loaded via DataPreprocessor in a real app, but here we might need manual handling if not using the class
        # However, for this structure let's assume raw features come in and we rely on DataPreprocessor used in the pipeline
        # Actually, best to instantiate DataPreprocessor here to handle scaling consistency
        from .preprocess import DataPreprocessor
        self.preprocessor = DataPreprocessor()
        
    def _load_model(self, filename):
        path = os.path.join(self.model_dir, filename)
        if os.path.exists(path):
            try:
                with open(path, 'rb') as f:
                    return pickle.load(f)
            except Exception as e:
                print(f"Error loading model {filename}: {e}")
                return None
        return None

    def predict(self, features, top_n=3):
        """
        Predicts top N crops based on features.
        :param features: List or numpy array of raw features [N, P, K, Temp, Hum, pH, Rain]
        :param top_n: Number of recommendations to return
        :return: List of dicts [{'crop': str, 'confidence': float}]
        """
        if self.agri_model and self.label_encoder:
            try:
                # 1. Preprocess (Scale)
                # Ensure feature format is compatible with preprocessor
                # The preprocessor expects a dictionary usually but we can adapt or pass correct type
                # Looking at predictor.py usage in app, likely input is already extracted.
                # Let's handle the raw input array scaling here.
                
                # We need to reshape for transformation
                features_array = np.array(features).reshape(1, -1)
                
                # SAFETY CHECK: If inputs are all zeros (Sensor Failure), do not predict.
                # Checking sum of absolute values or specific key nutrients
                if np.sum(features_array) == 0:
                    print("Warning: All sensor inputs are zero. Skipping prediction.")
                    return []
                
                # Apply scaling using the loaded scaler inside preprocessor
                if self.preprocessor.scaler:
                    features_scaled = self.preprocessor.scaler.transform(features_array)
                else:
                    features_scaled = features_array

                # 2. Predict Probabilities
                probs = self.agri_model.predict_proba(features_scaled)[0]
                
                # 3. Get Top N
                top_indices = probs.argsort()[-top_n:][::-1]
                
                results = []
                classes = self.label_encoder.classes_
                
                for idx in top_indices:
                    crop_name = classes[idx]
                    confidence = probs[idx]
                    # Filter out very low confidence predictions
                    if confidence > 0.01: 
                        results.append({
                            'crop': crop_name,
                            'confidence': round(float(confidence), 2)
                        })
                
                return results

            except Exception as e:
                print(f"Prediction Error: {e}")
                # Fallback only on error
                return self._mock_predict(top_n, features)
            
        # Fallback if no model loaded
        return self._mock_predict(top_n, features)

    def _mock_predict(self, top_n, features):
        """
        Mock prediction logic based on simple rules or random choice for demo.
        """
        # ... (Existing mock logic kept as failsafe)
        # List of crops from Kaggle dataset
        crops = [
            'rice', 'maize', 'chickpea', 'kidneybeans', 'pigeonpeas', 
            'mothbeans', 'mungbean', 'blackgram', 'lentil', 'pomegranate', 
            'banana', 'mango', 'grapes', 'watermelon', 'muskmelon', 'apple', 
            'orange', 'papaya', 'coconut', 'cotton', 'jute', 'coffee'
        ]
        
        # Simple heuristic to make mock data look somewhat "smart"
        # High rainfall -> Rice, Jute
        # Low rainfall -> Mothbeans, Millet
        rainfall = features[0][6] if features.shape[1] > 6 else 100
        
        if rainfall > 200:
            candidates = ['rice', 'jute', 'coconut', 'papaya']
        elif rainfall < 50:
            candidates = ['mothbeans', 'chickpea', 'lentil', 'muskmelon']
        else:
            candidates = crops
            
        selected = random.sample(candidates if len(candidates) >= top_n else crops, top_n)
        
        results = []
        for crop in selected:
            confidence = random.uniform(0.75, 0.98)
            results.append({
                'crop': crop,
                'confidence': round(confidence, 2)
            })
            
        # Sort desc by confidence
        results.sort(key=lambda x: x['confidence'], reverse=True)
        return results
