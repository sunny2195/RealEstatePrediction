from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir: Path
    source_data_path: Path
    local_data_file: Path


@dataclass(frozen=True)
class DataValidationConfig:
    root_dir: Path
    data_to_validate: Path
    status_file: Path
    all_schema: dict 


@dataclass(frozen=True)
class DataTransformationConfig:
    root_dir: Path
    data_to_transform: Path
    train_data_path: Path
    test_data_path: Path
    preprocessor_obj_file: Path
    target_column: str


@dataclass(frozen=True)
class ModelTrainerConfig:
    root_dir: Path
    train_data_path: Path
    model_file_path: Path


@dataclass(frozen=True)
class ModelEvaluationConfig:
    root_dir: Path
    test_data_path: Path
    model_path: Path
    metrics_file_path: Path
    target_column: str