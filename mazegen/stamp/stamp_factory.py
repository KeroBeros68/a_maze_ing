"""Factory for selecting and instantiating stamp designs.

This module provides the StampFactory class which implements the Factory
design pattern to create stamp design instances based on configuration.

Classes:
    StampFactory: Factory for creating stamp design instances
"""

from mazegen.stamp.stamp_design import StampDesign


class StampFactory:
    """Factory for creating stamp design instances.

    Provides a centralized way to instantiate stamp designs based on their
    name, allowing new stamp designs to be added without modifying existing code.

    Class Attributes:
        __designs: Dictionary mapping design names to design classes
    """

    __designs: dict[str, type[StampDesign]] = {}

    @classmethod
    def _init_designs(cls) -> None:
        """Lazy load stamp designs to avoid circular imports."""
        if not cls.__designs:
            try:
                from mazegen.stamp.forty_two_stamp import (
                    FortyTwoVanillaStamp,
                    FortyTwoCustomStamp,
                )
                cls.__designs = {
                    "42vanilla": FortyTwoVanillaStamp,
                    "42custom": FortyTwoCustomStamp,
                }
            except ImportError as e:
                raise RuntimeError(
                    f"Failed to initialize stamp designs: {e}"
                ) from e
            except Exception as e:
                raise RuntimeError(
                    f"Unexpected error during stamp design initialization: {e}"
                ) from e

    @classmethod
    def create(cls, design_name: str) -> StampDesign:
        """Create a stamp design instance by name.

        Args:
            design_name: Name of the stamp design to create
                        (case-insensitive)

        Returns:
            StampDesign: An instance of the requested stamp design

        Raises:
            ValueError: If design name is not registered
        """
        cls._init_designs()
        design_name_lower = design_name.lower().strip()

        if design_name_lower not in cls.__designs:
            available = ", ".join(cls.__designs.keys())
            raise ValueError(
                f"Stamp design '{design_name}' not found. "
                f"Available designs: {available}"
            )

        design_class = cls.__designs[design_name_lower]
        return design_class()

    @classmethod
    def register(cls, name: str, design_class: type[StampDesign]) -> None:
        """Register a new stamp design in the factory.

        This allows external code to register custom stamp designs
        without modifying the factory itself.

        Args:
            name: Name identifier for the design
            design_class: The design class to register

        Raises:
            TypeError: If design_class doesn't implement StampDesign
        """
        if not issubclass(design_class, StampDesign):
            raise TypeError(
                f"{design_class.__name__} must inherit from StampDesign"
            )

        cls._init_designs()
        cls.__designs[name.lower()] = design_class

    @classmethod
    def get_available_designs(cls) -> list[str]:
        """Get list of available stamp design names.

        Returns:
            list[str]: Names of all registered stamp designs
        """
        cls._init_designs()
        return list(cls.__designs.keys())
