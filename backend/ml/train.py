import pandas as pd
import numpy as np
import pickle
import os
import sys
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder

# Adjust path to import local modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from data_handler import DataHandler
from preprocess import DataPreprocessor

def train_models():
    print("Loading data...")
    handler = DataHandler()
    df = handler.load_data()
    
    if df is None or df.empty:
        print("No data available for training.")
        return

    # Split features and target
    X = df.drop('label', axis=1)
    y = df['label']

    # Preprocessing (Scaling)
    print("Preprocessing data...")
    preprocessor = DataPreprocessor()
    preprocessor.fit_and_save(X) # Saves scaler
    # Transform training data using the fitted scaler
    X_scaled = preprocessor.scaler.transform(X)
    
    # Label Encoding for Target
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)
    
    # Save LabelEncoder
    current_dir = os.path.dirname(os.path.abspath(__file__))
    model_dir = os.path.join(os.path.dirname(current_dir), 'models')
    
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)
    with open(os.path.join(model_dir, 'label_encoder.pkl'), 'wb') as f:
        pickle.dump(le, f)

    # Train Test Split
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_encoded, test_size=0.2, random_state=42)

    # Define Models
    models = {
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
        'Gradient Boosting': GradientBoostingClassifier(random_state=42),
        'Naive Bayes': GaussianNB(),
        'SVM': SVC(probability=True, random_state=42) # probability=True for predict_proba
    }

    best_model = None
    best_accuracy = 0.0
    best_model_name = ""

    print("\nTraining Models:")
    print("-" * 30)

    for name, model in models.items():
        try:
            model.fit(X_train, y_train)
            predictions = model.predict(X_test)
            acc = accuracy_score(y_test, predictions)
            print(f"{name}: {acc:.4f} accuracy")
            
            if acc > best_accuracy:
                best_accuracy = acc
                best_model = model
                best_model_name = name
        except Exception as e:
            print(f"Error training {name}: {e}")

    print("-" * 30)
    print(f"Best Model: {best_model_name} with {best_accuracy:.4f} accuracy")

    # Save Best Model
    if best_model:
        model_path = os.path.join(model_dir, 'crop_recommendation_model.pkl')
        with open(model_path, 'wb') as f:
            pickle.dump(best_model, f)
        print(f"Best model saved to {model_path}")

if __name__ == "__main__":
    train_models()
