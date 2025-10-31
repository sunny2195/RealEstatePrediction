import pandas as pd
import os
from housing_pricer.config.configuration import ConfigurationManager
from housing_pricer.entity.config_entity import DataValidationConfig
from pathlib import Path

class DataValidation:
    def __init__(self, config: DataValidationConfig):
        self.config = config

    def validate_all_columns(self) -> bool:
        try:
            os.makedirs(self.config.root_dir, exist_ok=True)
            validation_status = True  # Assume PASS until a failure
            data = pd.read_csv(self.config.data_to_validate)
            all_cols = list(data.columns)
            all_schema = self.config.all_schema.keys()
            print("--- Starting Column Validation ---")

            if len(all_cols) != len(all_schema):
                validation_status = False
                print(f"VALIDATION: FAIL! Column count mismatch. Expected {len(all_schema)}, got {len(all_cols)}")

            for col, dtype in self.config.all_schema.items():
                if col not in all_cols:
                    validation_status = False
                    print(f"VALIDATION: FAIL! Required column '{col}' is missing.")
                elif data[col].dtype != dtype:
                    validation_status = False
                    print(f"VALIDATION: FAIL! Column '{col}' has wrong type. Expected {dtype}, got {data[col].dtype}")

            if validation_status:
                print("--- Column Validation: PASS ---")

            with open(self.config.status_file, 'w') as f:
                f.write(f"Validation Status: {'PASS' if validation_status else 'FAIL'}")

            return validation_status

        except Exception as e:
            os.makedirs(self.config.root_dir, exist_ok=True)
            
            with open(self.config.status_file, 'w') as f:
                f.write(f"Validation Status: FAIL (Error: {e})")
            print(f"Error during validation: {e}")
            return False
        
    def run_validation(self) -> bool:
        """
        Main "manager" function for this component.
        """
        print("--- Starting Data Validation Component ---")
        validation_status= self.validate_all_columns()
        print("--- Data Validation Component Complete ---")

        return validation_status





