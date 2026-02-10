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
from model import ConfigModel  # noqa: E402
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

print(config)
print()

control = Controller(config)

with control as c:
    c.process()

# try:
#     maze = maze_generator.generate_maze()
# except Exception as e:
#     print(e)
#     sys.exit(1)

# try:
#     control.start()
#     print("✓ Keyboard input mode enabled")
#     print("Press any key...\n")

#     while True:
#         key = control.poll()

#         if key is not None:
#             if key == "q":
#                 print("Quit requested")
#                 break
#             elif key == "\x03":  # Ctrl+C
#                 print("\nCtrl+C detected")
#                 break
#             elif ord(key) == 27:  # Escape
#                 print("Escape detected")
#                 break
#             else:
#                 print(f"Key pressed: '{key}' (code: {ord(key)})")

#         time.sleep(0.05)  # Small delay to prevent tight loop

# except KeyControlError as e:
#     print(f"✗ Error: {e}", file=sys.stderr)
#     sys.exit(1)
# finally:
#     terminal_manager.cleanup()
#     print("✓ Terminal restored")

# maze_generator.create_output_file()
