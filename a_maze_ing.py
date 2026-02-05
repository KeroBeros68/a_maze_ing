"""
Maze generator application.

This module initializes the maze generation application by:
- Checking the Python environment and dependencies
- Loading configuration from config.txt
- Validating configuration parameters using Pydantic
- Initializing the maze generator with validated configuration

Dependencies:
    - pydantic: Data validation and parsing
    - pydantic_settings: Configuration file loading and validation
"""

from typing import Dict
import env_check
from model import ConfigModel
import sys


module_list: Dict[str, Dict[str, str]] = {
    "pydantic": {
        "package": "pydantic",
        "message": "Data validation ready",
    },
    "pydantic_settings": {
        "package": "pydantic_settings",
        "message": "Read config file ready",
    },
}

check_env = env_check.EnvCheck(module_list)

check_env.check_process()

from pydantic import ValidationError  # noqa: E402


print("\n===== A_maze_ing =====\n")
try:
    config = ConfigModel()  # type: ignore[call-arg]
except ValidationError as e:
    for error in e.errors():
        field = error["loc"][0] if error["loc"] else "model"
        print(f"Field: {field}")
        print(f"Error: {error['msg']}")
        print(f"Type: {error['type']}\n")
    sys.exit(1)

print(config.ENTRY)
