from housing_pricer.utils.common import read_yaml
from housing_pricer.entity.config_entity import (
    DataIngestionConfig,
    DataValidationConfig,
    DataTransformationConfig,
    ModelTrainerConfig,
    ModelEvaluationConfig
)
from pathlib import Path

CONFIG_FILE_PATH = Path("config/config.yaml")

class ConfigurationManager:
    def __init__(self, config_filepath = CONFIG_FILE_PATH):
        self.config = read_yaml(config_filepath)
    
    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config.data_ingestion
        data_ingestion_config = DataIngestionConfig(
            root_dir=Path(config.root_dir),
            source_data_path=Path(config.source_data_path),
            local_data_file=Path(config.local_data_file)
        )

        return data_ingestion_config
    
    def get_data_validation_config(self) -> DataValidationConfig:
        config = self.config.data_validation

        manual_schema = {
            "Suburb": "object",
            "Address": "object",
            "Rooms": "int64",
            "Type": "object",
            "Price": "float64",
            "Method": "object",
            "SellerG": "object",
            "Date": "object",
            "Postcode": "int64",
            "Regionname": "object",
            "Propertycount": "int64",
            "Distance": "float64",
            "CouncilArea": "object"
        }

        data_validation_config = DataValidationConfig(
            root_dir=Path(config.root_dir),
            data_to_validate=Path(config.data_to_validate),
            status_file=Path(config.status_file),
            all_schema=manual_schema  
        )

        return data_validation_config

    def get_data_transformation_config(self) -> DataTransformationConfig:

        config = self.config.data_transformation

        data_transformation_config = DataTransformationConfig(
            root_dir=Path(config.root_dir),
            data_to_transform=Path(config.data_to_transform),
            train_data_path=Path(config.train_data_path),
            test_data_path=Path(config.test_data_path),
            preprocessor_obj_file=Path(config.preprocessor_obj_file),
            target_column="Price"

            )

        return data_transformation_config

    def get_model_trainer_config(self) -> ModelTrainerConfig:

        config = self.config.model_trainer

        model_trainer_config = ModelTrainerConfig(
            root_dir=Path(config.root_dir),
            train_data_path=Path(config.train_data_path),
            model_file_path=Path(config.model_file_path)
        )

        return model_trainer_config

    def get_model_evaluation_config(self) -> ModelEvaluationConfig:

        config = self.config.model_evaluation

        model_evaluation_config = ModelEvaluationConfig(
            root_dir=Path(config.root_dir),
            test_data_path=Path(config.test_data_path),
            model_path=Path(config.model_path),
            metrics_file_path=Path(config.metrics_file_path),
            target_column="Price"
        )
        return model_evaluation_config