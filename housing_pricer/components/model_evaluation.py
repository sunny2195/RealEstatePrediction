import os
import pandas as pd
import joblib
import json
import numpy as np
from sklearn.metrics import mean_squared_error, r2_score
from housing_pricer.config.configuration import ConfigurationManager
from housing_pricer.entity.config_entity import ModelEvaluationConfig
from pathlib import Path

class ModelEvaluation:
    def __init__(self, config: ModelEvaluationConfig):
        self.config = config

    def evaluate_model(self):
        try:
            test_df = pd.read_csv(self.config.test_data_path)
            print(f"Loaded test data: {self.config.test_data_path}")

            model = joblib.load(self.config.model_path)
            print(f"Loaded model from: {self.config.model_path}")

            preprocessor_path = Path(self.config.model_path).parent.parent / "data_transformation/preprocessor.pkl"
            preprocessor = joblib.load(preprocessor_path)
            print(f"Loaded preprocessor from: {preprocessor_path}")

            X_test = test_df.drop(self.config.target_column, axis=1)
            y_test = test_df[self.config.target_column]

            X_test_transformed = preprocessor.transform(X_test)
            print("Test data features transformed successfully.")

            predictions = model.predict(X_test_transformed)
            print("Predictions generated on test set.")

            rmse = np.sqrt(mean_squared_error(y_test, predictions))
            r2 = r2_score(y_test, predictions)

            print(f"--- Model Report Card ---")
            print(f"  RMSE: {rmse:.2f}")
            print(f"  R-Squared: {r2:.3f}")
            print(f"-------------------------")

            metrics = {"rmse": rmse, "r2_score": r2}
            os.makedirs(self.config.root_dir, exist_ok=True)
            with open(self.config.metrics_file_path, 'w') as f:
                json.dump(metrics, f, indent=4)
            
            print(f"Metrics saved to: {self.config.metrics_file_path}")

        except Exception as e:
            print(f"Error during model evaluation: {e}")
            raise e
        
    def run_evaluation(self):
        """
        Main "manager" function for this component.
        """
        print("--- Starting Model Evaluation Component ---")
        self.evaluate_model()
        print("--- Model Evaluation Component Complete ---")