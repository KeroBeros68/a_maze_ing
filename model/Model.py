"""
Configuration model for maze generation.

This module defines the Pydantic configuration model that validates
maze generation parameters from the config.txt file.

The model ensures:
- Valid maze dimensions (width and height)
- Valid entry and exit coordinates within bounds
- Entry and exit are different points
- Output file name is valid
- Algorithm name is valid

Classes:
    ConfigModel: Pydantic BaseSettings model for maze configuration
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, model_validator
from typing import Optional, Tuple


class ConfigModel(BaseSettings):
    """Pydantic configuration model for maze generation settings.

    Validates and loads maze generation parameters from config.txt file.
    Ensures all configuration values are within valid ranges and
    coordinates are consistent.

    Attributes:
        WIDTH: Width of the maze (0-200)
        HEIGHT: Height of the maze (0-200)
        ENTRY: Entry point coordinates (x, y)
        EXIT: Exit point coordinates (x, y)
        OUTPUT_FILE: Path to output file for generated maze
        PERFECT: Whether to generate perfect maze (no loops)
        ALGORITHM: Maze generation algorithm name
        SEED: Random seed for reproducible generation
        MODE_GEN: Generation mode ("normal" or "animated")
        DISPLAY_MODE: Display mode ("basic", "tty", or "mlx")
    """
    model_config = SettingsConfigDict(env_file="config.txt")

    WIDTH: int = Field(..., ge=0, le=200, description="Width of the maze")
    HEIGHT: int = Field(..., ge=0, le=200, description="Height of the maze")
    ENTRY: Tuple[int, int] = Field(..., description="Entry coordinates (x, y)")
    EXIT: Tuple[int, int] = Field(..., description="Exit coordinates (x, y)")
    OUTPUT_FILE: str = Field(
        ..., min_length=4, max_length=15, description="Output file name"
    )
    PERFECT: bool = Field(default=False, description="Generate a perfect maze")
    ALGORITHM: str = Field(
        default="backtracking", description="Maze generation algorithm to use"
    )
    SEED: Optional[str] = Field(
        default=None,
        min_length=0,
        max_length=100,
        description="Seed generation",
    )
    MODE_GEN: str = Field(
        default="normal",
        description="Generation mode: " "'normal' or 'animated'",
    )
    DISPLAY_MODE: str = Field(
        default="basic", description="Display mode (basic, tty, mlx)"
    )

    @model_validator(mode="after")
    def validate_entry_exit(self) -> "ConfigModel":
        """
        Validate entry and exit coordinates.

        Ensures that:
        - Entry and exit coordinates are non-negative
        - Entry and exit coordinates are different
        - Coordinates are within maze bounds (width and height)

        Returns:
            ConfigModel: The validated configuration model

        Raises:
            ValueError: If any coordinate validation fails
        """
        x1, y1 = self.ENTRY
        x2, y2 = self.EXIT

        # Check coordinates are not negative
        if x1 < 0 or y1 < 0 or x2 < 0 or y2 < 0:
            raise ValueError("Entry and Exit coordinates must be non-negative")

        # Check they are different
        if self.ENTRY == self.EXIT:
            raise ValueError(
                "Exit coordinates cannot be " "the same as Entry coordinates"
            )

        # Check they are within bounds
        if x1 >= self.WIDTH or x2 >= self.WIDTH:
            raise ValueError(
                f"Entry or Exit X coordinate exceeds width ({self.WIDTH})"
            )
        if y1 >= self.HEIGHT or y2 >= self.HEIGHT:
            raise ValueError(
                f"Entry or Exit Y coordinate exceeds height ({self.HEIGHT})"
            )

        return self
