import os
import pandas as pd
from housing_pricer.config.configuration import ConfigurationManager
from housing_pricer.entity.config_entity import ModelTrainerConfig
import lightgbm as lgb
from pathlib import Path
import joblib


class ModelTrainer:
    def __init__(self, config: ModelTrainerConfig):
        self.config = config

    def run_training(self):
        print("--- Starting Model Trainer Component ---")
        try:
            os.makedirs(self.config.root_dir, exist_ok=True)
            train_df = pd.read_csv(self.config.train_data_path)
            print(f"Loaded training data: {self.config.train_data_path}")

            preprocessor_path = Path(self.config.root_dir).parent / "data_transformation/preprocessor.pkl"
            preprocessor = joblib.load(preprocessor_path)
            print(f"Loaded preprocessor from: {preprocessor_path}")

            target_column = "Price" # This should come from config, but we'll hard-code
            X_train = train_df.drop(target_column, axis=1)
            y_train = train_df[target_column]

            X_train_transformed = preprocessor.transform(X_train)
            print("Training data features transformed successfully.")

            print("Training LGBMRegressor model...")
            model = lgb.LGBMRegressor(random_state=42)

            model.fit(X_train_transformed, y_train)
            print("Model training complete.")

            joblib.dump(model, self.config.model_file_path)
            print(f"Trained model saved to: {self.config.model_file_path}")

            print("--- Model Trainer Component Complete ---")

        except Exception as e:
            print(f"Error during model training: {e}")
            raise e





