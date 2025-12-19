import pandas as pd
import os
import sys

class DataHandler:
    def __init__(self):
        # Determine the root directory (assuming this script is in backend/ml/)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Path to 'd:\Projects\mitti mitra\data\Crop_recommendation.csv'
        # Go up two levels from backend/ml to project root, then into data
        self.data_path = os.path.join(os.path.dirname(os.path.dirname(current_dir)), 'data', 'Crop_recommendation.csv')

    def load_data(self):
        """
        Loads the crop recommendation dataset.
        Returns:
            pd.DataFrame: Cleaned dataframe ready for training.
        """
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"Dataset not found at {self.data_path}")

        try:
            df = pd.read_csv(self.data_path)
            
            # 1. Drop rows where ALL columns are missing
            df.dropna(how='all', inplace=True)
            
            # 2. Impute missing values for feature columns
            # Assuming 'label' is the target column
            if 'label' in df.columns:
                target = df['label']
                features = df.drop(columns=['label'])
                
                # Impute numeric features with mean
                from sklearn.impute import SimpleImputer
                imputer = SimpleImputer(strategy='mean')
                features_imputed = pd.DataFrame(imputer.fit_transform(features), columns=features.columns)
                
                # Recombine
                df_clean = pd.concat([features_imputed, target.reset_index(drop=True)], axis=1)
                return df_clean
            
            return df
        except Exception as e:
            print(f"Error loading data: {e}")
            return None
