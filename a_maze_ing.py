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
import utils.env_check as env_check
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
from model.Model import ConfigModel  # noqa: E402
from controller import Controller  # noqa: E402


print("\n===== A_maze_ing =====\n")
try:
    config = ConfigModel()  # type: ignore[call-arg]
except ValidationError as e:
    for error in e.errors():
        field = error["loc"][0] if error["loc"] else "model"
        sys.stderr.write(f"Field: {field}")
        sys.stderr.write(f"Error: {error['msg']}")
        sys.stderr.write(f"Type: {error['type']}\n")
    sys.exit(1)

control = Controller(config)

try:
    with control as c:
        c.process()
except Exception as e:
    print("error:", {e}, file=sys.stderr)
