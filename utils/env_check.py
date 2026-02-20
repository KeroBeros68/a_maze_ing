"""
Detect and display Python virtual environment status.

This module demonstrates understanding of Python virtual environments by:
- Detecting whether code runs in a venv or global Python
- Displaying environment-specific information
- Providing setup instructions for virtual environments
"""

import site
import sys
import os
import time
from importlib import import_module, metadata
from typing import Dict


class EnvCheck():
    """
    Manage and validate Python virtual environment and dependencies.

    This class handles:
    - Detection of active virtual environment
    - Validation of required packages installation
    - User-friendly error messages and setup instructions

    Attributes:
        module_list: Dictionary containing package names and their descriptions
    """

    def __init__(self, module_list: Dict[str, Dict[str, str]]):
        """
        Initialize EnvCheck with required modules list.

        Args:
            module_list: Dictionary with package info containing:
                - 'package': package name for pip
                - 'message': description of package purpose
        """
        self.module_list: Dict[str, Dict[str, str]] = module_list

    def check_process(self) -> None:
        """
        Main process to check environment and dependencies.

        Verifies that the script runs in a virtual environment and
        validates that all required dependencies are installed.
        Exits with code 1 if environment or dependencies are invalid.
        """
        virtual_env: str | None = os.environ.get("VIRTUAL_ENV")
        try:
            if sys.prefix == sys.base_prefix and not virtual_env:
                self.reality_process(virtual_env)
                sys.exit(1)
            else:
                self.virtual_process(virtual_env)
                if not self.check_dependencies():
                    sys.exit(1)
        except Exception as e:
            sys.stderr.write(f"Error: {e}")

    @staticmethod
    def virtual_process(virtual_env: str | None) -> None:
        """
        Display virtual environment information and success message.

        When running inside a virtual environment, this function shows:
        - Current Python executable path
        - Virtual environment name and path
        - Location of site-packages directory
        - Security confirmation of isolated environment

        Args:
            virtual_env: Path to the active virtual environment from
            VIRTUAL_ENV

        Returns:
            None - prints information to stdout
        """
        print("\nMATRIX STATUS: Welcome to the construct\n")
        print("Current Python:", sys.executable)
        venv_name: str = (os.path.basename(virtual_env) if virtual_env
                          else "unknown")
        print(f"Virtual Environment: {venv_name}")
        print(f"Environment Path: {virtual_env}\n")
        print(
            "SUCCESS: You're in an isolated environment!\n"
            "Safe to install packages without affecting\n"
            "the global system.\n"
        )

        print("Package installation path:")
        if virtual_env:
            site_packages_path: str = os.path.join(
                virtual_env, "lib", "python3.13", "site-packages"
            )
            print(site_packages_path)
        else:
            for s in site.getsitepackages():
                print(s)

    @staticmethod
    def reality_process(virtual_env: str | None) -> None:
        """
        Display global environment warning and setup instructions.

        When running in the global Python environment (no venv detected),
        this function warns the user about the security risks and provides
        clear instructions for creating and activating a virtual environment.

        Args:
            virtual_env: Value of VIRTUAL_ENV (should be None in global env)

        Returns:
            None - prints warning and instructions to stdout
        """
        print("\nMATRIX STATUS: You're still plugged in\n")
        print("Current Python:", sys.executable)
        print(f"Virtual Environment: {virtual_env} detected")
        print(
            "WARNING: You're in the global environment!\n"
            "The machines can see everything you install.\n"
        )
        print(
            "To enter the construct, run:\n"
            "python -m venv matrix_env\n"
            "source matrix_env/bin/activate # On Unix\n"
            "matrix_env\n"
            "Scripts\n"
            "activate # On Windows\n"
        )
        print("Then run this program again.")

    def check_dependencies(self) -> bool:
        """
        Verify that all required packages are installed.

        Iterates through module_list, attempting to import each package
        and retrieve its version from package metadata.

        Returns:
            bool: True if all dependencies loaded, False if any are missing
        """

        print("LOADING STATUS: Loading programs...\n")
        print("Checking dependencies:")
        all_loaded: bool = True

        for module_name, info in self.module_list.items():
            spinner = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
            for frame in spinner:
                sys.stdout.write(f"\r    {frame} Loading {module_name}...")
                sys.stdout.flush()
                time.sleep(0.05)

            try:
                import_module(module_name)
                meta = metadata.metadata(info["package"])
                print(
                    f"\r    [OK] {meta['Name']} ({meta['Version']}) -"
                    f" {info['message']}"
                )
            except ModuleNotFoundError:
                all_loaded = False
                print(
                    f"\r    [NOK] ERROR: Program '{module_name}' not loaded. "
                    "Please use pip or poetry to install dependencies."
                )

        return all_loaded
