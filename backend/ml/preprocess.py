import numpy as np
import os
import pickle
from sklearn.preprocessing import StandardScaler

class DataPreprocessor:
    def __init__(self):
        """
        Initialize preprocessor. 
        """
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.model_dir = os.path.join(os.path.dirname(current_dir), 'models')
        self.scaler_path = os.path.join(self.model_dir, 'scaler.pkl')
        self.scaler = self._load_scaler()

    def _load_scaler(self):
        if os.path.exists(self.scaler_path):
            try:
                with open(self.scaler_path, 'rb') as f:
                    return pickle.load(f)
            except Exception as e:
                print(f"Error loading scaler: {e}")
        return None

    def fit_and_save(self, data):
        """
        Fits a new scaler on the provided data and saves it.
        :param data: Numpy array or DataFrame of features (no labels)
        """
        scaler = StandardScaler()
        scaler.fit(data)
        
        if not os.path.exists(self.model_dir):
            os.makedirs(self.model_dir)
            
        with open(self.scaler_path, 'wb') as f:
            pickle.dump(scaler, f)
            
        self.scaler = scaler
        print(f"Scaler saved to {self.scaler_path}")

    def preprocess(self, data):
        """
        Converts input dictionary to model-ready numpy array.
        Expected input format matches the dataset feature order:
        [N, P, K, temperature, humidity, ph, rainfall]
        
        :param data: Dictionary with keys 'N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall'
        :return: 2D numpy array (1, 7) scaled if scaler exists
        """
        try:
            features = [
                float(data.get('N', 0)),
                float(data.get('P', 0)),
                float(data.get('K', 0)),
                float(data.get('temperature', 0)),
                float(data.get('humidity', 0)),
                float(data.get('ph', 0)),
                float(data.get('rainfall', 0))
            ]
            
            features_array = np.array([features])
            
            if self.scaler:
                 return self.scaler.transform(features_array)
            
            return features_array
            
        except Exception as e:
            print(f"Error in preprocessing: {e}")
            raise ValueError(f"Preprocessing Failed: {e}")
