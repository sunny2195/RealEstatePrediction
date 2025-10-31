from dataclasses import dataclass
from pathlib import Path

# Note: '@dataclass' is a "decorator" that automatically adds
# basic functions to our class (like __init__) so we don't 
# have to write them. It's just a clean way to define a 
# class that holds data.

@dataclass(frozen=True)
class DataIngestionConfig:
    """
    This is the blueprint for our Data Ingestion settings.
    frozen=True means these objects are "read-only" after
    they are created, which prevents accidental bugs.
    """
    root_dir: Path
    source_data_path: Path
    local_data_file: Path


@dataclass(frozen=True)
class DataValidationConfig:
    """
    Blueprint for Data Validation settings.
    """
    root_dir: Path
    data_to_validate: Path
    status_file: Path
    # Since we skipped schema.yaml, we'll define our 
    # expected columns and types right here.
    all_schema: dict 


@dataclass(frozen=True)
class DataTransformationConfig:
    """
    Blueprint for Data Transformation settings.
    """
    root_dir: Path
    data_to_transform: Path
    train_data_path: Path
    test_data_path: Path
    preprocessor_obj_file: Path
    # We will also define our target column here.
    target_column: str


@dataclass(frozen=True)
class ModelTrainerConfig:
    """
    Blueprint for Model Trainer settings.
    """
    root_dir: Path
    train_data_path: Path
    model_file_path: Path


@dataclass(frozen=True)
class ModelEvaluationConfig:
    """
    Blueprint for Model Evaluation settings.
    """
    root_dir: Path
    test_data_path: Path
    model_path: Path
    metrics_file_path: Path
    target_column: str