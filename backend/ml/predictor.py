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
        
        self.agri_model = self._load_model('agricultural_model.pkl')
        self.horti_model = self._load_model('horticultural_model.pkl')
        
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
        :param features: Preprocessed numpy array (1, 7)
        :param top_n: Number of recommendations to return
        :return: List of dicts [{'crop': str, 'confidence': float}]
        """
        if self.agri_model:
            # TODO: Implement real prediction logic using standard sklearn predict_proba
            # classes = self.agri_model.classes_
            # probabilities = self.agri_model.predict_proba(features)[0]
            # ... map to crop names ...
            pass
            
        # Fallback to Mock logic if models are not present or for this demo phase
        return self._mock_predict(top_n, features)

    def _mock_predict(self, top_n, features):
        """
        Mock prediction logic based on simple rules or random choice for demo.
        """
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
