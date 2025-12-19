import pandas as pd
import numpy as np
import pickle
import os

# Mock Dataset
data = {
    'N': [90, 85, 60, 74, 78],
    'P': [42, 58, 55, 35, 42],
    'K': [43, 41, 44, 40, 42],
    'temperature': [20.8, 21.7, 23.0, 26.4, 20.1],
    'humidity': [82.0, 80.3, 80.6, 80.1, 81.6],
    'ph': [6.5, 7.0, 7.8, 6.9, 7.6],
    'rainfall': [202.9, 226.6, 263.9, 242.8, 262.7],
    'label': ['rice', 'rice', 'jute', 'maize', 'rice']
}

df = pd.DataFrame(data)

print("Training model...")
# In a real scenario, we would train a RandomForestClassifier here.
# For this demo, we will just save a dummy model or just rely on the predict script logic.

model_path = 'models/crop_recommendation_model.pkl'
if not os.path.exists('models'):
    os.makedirs('models')

with open(model_path, 'wb') as f:
    pickle.dump(df, f) # Dumping dataframe as a dummy model

print(f"Model saved to {model_path}")
