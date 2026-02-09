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
from mazegen.utils.model import ConfigModel  # noqa: E402
from mazegen.MazeGenerator import MazeGenerator  # noqa: E402


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

print(config)
print()

maze_generator = MazeGenerator(config)

try:
    maze = maze_generator.generate_maze()
except Exception as e:
    print(e)
    sys.exit(1)

print("\33[1m")
print(maze)
print("\33[0m")

print("\nSEED =", config.SEED)
maze_generator.create_output_file()
