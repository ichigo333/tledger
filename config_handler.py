import os
import json
from typing import Dict


CONFIG_FILE_NAME = "config.json"


def load_config() -> Dict[str, str]:
    base_dir = os.path.dirname(__file__)
    config_file_path = os.path.join(base_dir, CONFIG_FILE_NAME)

    try:
        with open(config_file_path, "r") as file:
            print(f"Loading config: {config_file_path}")
            return json.load(file)
    except Exception as e:
        print(f"Error loading config, using defaults")
        print(f"Error: {e}")

        return {
            "data_dir": "data/",
        }
