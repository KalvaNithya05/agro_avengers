import numpy as np
import os

class DataPreprocessor:
    def __init__(self):
        """
        Initialize preprocessor. 
        In production, this would load a saved StandardScaler/MinMaxScaler.
        """
        # self.scaler = load_scaler()
        pass

    def preprocess(self, data):
        """
        Converts input dictionary to model-ready numpy array.
        Expected input format matches the Kaggle dataset feature order:
        [N, P, K, temperature, humidity, ph, rainfall]
        
        :param data: Dictionary with keys 'N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall'
        :return: 2D numpy array (1, 7)
        """
        try:
            # Ensure order matches training data exactly
            # N, P, K, Temp, Hum, pH, Rain
            features = [
                float(data.get('N', 0)),
                float(data.get('P', 0)),
                float(data.get('K', 0)),
                float(data.get('temperature', 0)),
                float(data.get('humidity', 0)),
                float(data.get('ph', 0)),
                float(data.get('rainfall', 0))
            ]
            
            # TODO: If using scaler, apply transform here
            # features_scaled = self.scaler.transform([features])
            # return features_scaled
            
            return np.array([features])
            
        except Exception as e:
            print(f"Error in preprocessing: {e}")
            raise ValueError(f"Preprocessing Failed: {e}")
