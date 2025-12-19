import pandas as pd
import numpy as np
import os
import sys
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler, LabelEncoder

import warnings
warnings.filterwarnings('ignore')

# Adjust path to import local modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from data_handler import DataHandler

def debug_analysis():
    print("Starting Deep Debug Analysis...")
    handler = DataHandler()
    df = handler.load_data()
    
    if df is None or df.empty:
        print("ERROR: No data loaded.")
        return

    # print(f"Dataset Shape: {df.shape}")
    # print(f"Columns: {df.columns.tolist()}")
    
    # Check Class Distribution
    # print("\nClass Distribution:")
    # print(df['label'].value_counts().head())
    
    # Split features and target
    X = df.drop('label', axis=1)
    y = df['label']
    
    # print("\nFeature Stats:")
    # print(X.describe())

    # Check for leakage: Is label somehow in X? (Already dropped, but good to double check column names)
    if 'label' in X.columns:
        print("CRITICAL ERROR: Label found in features!")
    else:
        print("Leakage Check: Passed")

    # Standard Scaling
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Label Encoding
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)
    
    # Cross Validation with Naive Bayes (Current Champion)
    # print("\nRunning 5-Fold Cross Validation (Naive Bayes)...")
    nb = GaussianNB()
    scores = cross_val_score(nb, X_scaled, y_encoded, cv=5, scoring='accuracy')
    # print(f"CV Scores: {scores}")
    print(f"Mean Accuracy: {scores.mean():.4f}")

    # Train/Test Split Report
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded)
    nb.fit(X_train, y_train)
    # preds = nb.predict(X_test)
    
    # print("\nClassification Report (Test Set):")
    # unique_labels = np.unique(np.concatenate((y_test, preds)))
    # target_names = le.inverse_transform(unique_labels)
    # print(classification_report(y_test, preds, target_names=target_names))
    
    print("\n--- Manual Prediction Tests ---")
    
    # Case 1: High Rainfall (Should be Rice/Jute)
    # sample_rice = np.array([[80, 40, 40, 20, 80, 7, 200]])
    # sample_rice_scaled = scaler.transform(sample_rice)
    # pred_rice = nb.predict_proba(sample_rice_scaled)[0]
    # top_idx = pred_rice.argsort()[-1]
    # print(f"Input: High Rainfall (Rice/Jute) -> Prediction: {le.inverse_transform([top_idx])[0]} (Conf: {pred_rice[top_idx]:.2f})")

    # Case 3: ZEROS (What happens if sensors fail?)
    sample_zero = np.array([[0, 0, 0, 0, 0, 0, 0]])
    sample_zero_scaled = scaler.transform(sample_zero)
    pred_zero = nb.predict_proba(sample_zero_scaled)[0]
    top_idx_zero = pred_zero.argsort()[-1]
    print(f"Input: ALL ZEROS               -> Prediction: {le.inverse_transform([top_idx_zero])[0]} (Conf: {pred_zero[top_idx_zero]:.2f})")

    
if __name__ == "__main__":
    debug_analysis()
