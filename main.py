from housing_pricer.config.configuration import ConfigurationManager
from housing_pricer.components.data_ingestion import DataIngestion
from housing_pricer.components.data_validation import DataValidation

class TrainingPipeline:
    def __init__(self):
        self.config_manager = ConfigurationManager()

    def run(self):
        try:
            print(">>> Starting Stage 1: Data Ingestion <<<")
            ingestion_config = self.config_manager.get_data_ingestion_config()
            data_ingestion = DataIngestion(config=ingestion_config)
            data_ingestion.run_ingestion()

            print(">>> Stage 1: Data Ingestion Complete <<<\n")

            print(">>> Starting Stage 2: Data Validation <<<")
            validation_config = self.config_manager.get_data_validation_config()
            data_validation = DataValidation(config=validation_config)

            if not data_validation.run_validation():
                raise Exception("Data Validation Failed. Pipeline stopped.")
            
            print(">>> Stage 2: Data Validation Complete <<<\n")




        except Exception as e:
            print(f"Training Pipeline Failed: {e}")
            raise e

if __name__ == "__main__":
    try:
        pipeline = TrainingPipeline()
        pipeline.run()
    except Exception as e:
        print(f"Training Pipeline Failed: {e}")