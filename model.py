"""
Configuration model for maze generation.

This module defines the Pydantic configuration model that validates
maze generation parameters from the config.txt file.

The model ensures:
- Valid maze dimensions (width and height)
- Valid entry and exit coordinates within bounds
- Entry and exit are different points
- Output file name is valid

Classes:
    ConfigModel: Pydantic BaseSettings model for maze configuration
"""

from pydantic_settings import BaseSettings
from pydantic import Field, model_validator
from typing import Tuple


class ConfigModel(BaseSettings):
    WIDTH: int = Field(..., ge=0, le=100, description="Width of the maze")
    HEIGHT: int = Field(..., ge=0, le=100, description="Height of the maze")
    ENTRY: Tuple[int, int] = Field(..., description="Entry coordinates (x, y)")
    EXIT: Tuple[int, int] = Field(..., description="Exit coordinates (x, y)")
    OUTPUT_FILE: str = Field(..., min_length=4, max_length=15,
                             description="Output file name")
    PERFECT: bool = Field(default=False, description="Generate a perfect maze")

    class Config:
        env_file = "config.txt"

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
            raise ValueError("Exit coordinates cannot be "
                             "the same as Entry coordinates")

        # Check they are within bounds
        if x1 >= self.WIDTH or x2 >= self.WIDTH:
            raise ValueError(
                f"Entry or Exit X coordinate exceeds width ({self.WIDTH})")
        if y1 >= self.HEIGHT or y2 >= self.HEIGHT:
            raise ValueError(
                f"Entry or Exit Y coordinate exceeds height ({self.HEIGHT})")

        return self
