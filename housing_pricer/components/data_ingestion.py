import os
import shutil
from pathlib import Path
from housing_pricer.config.configuration import ConfigurationManager
from housing_pricer.entity.config_entity import DataIngestionConfig

class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config

    def copy_source_data(self):
        try:
            os.makedirs(self.config.root_dir, exist_ok=True)

            print(f"Checking for source file at: {self.config.source_data_path}")
            if not os.path.exists(self.config.source_data_path):
                raise FileNotFoundError(
                    f"CRITICAL: Raw data file not found at {self.config.source_data_path}"
                )
            
            print(f"Copying data from {self.config.source_data_path} to {self.config.local_data_file}")
            shutil.copy(self.config.source_data_path, self.config.local_data_file)
            print("Copy complete.")

        except Exception as e:
            raise e

    def run_ingestion(self):
        print("--- Starting Data Ingestion Component ---")
        self.copy_source_data()
        print("--- Data Ingestion Component Complete ---")




