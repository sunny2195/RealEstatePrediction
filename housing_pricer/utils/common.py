import os
import yaml
from pathlib import Path
from box import ConfigBox
from box.exceptions import BoxValueError

def read_yaml(path_to_yaml: Path) -> ConfigBox:
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            print(f"YAML file '{path_to_yaml}' loaded successfully.")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError(f"YAML file '{path_to_yaml}' is empty.")
    except Exception as e:
        raise e
