"""Abstract interface for stamp designs.

This module defines the StampDesign abstract base class that all stamp
designs must implement, enabling extensibility of the stamping system.

Classes:
    StampDesign: Abstract base class for stamp designs
"""

from abc import ABC, abstractmethod
from typing import List


class StampDesign(ABC):
    """Abstract base class for stamp designs.

    Defines the contract that all stamp designs must follow, including
    providing logos in different sizes.
    """

    @abstractmethod
    def get_logo(self, size: int) -> List[str]:
        """Get a logo design for the given size.

        Args:
            size: Requested size of the logo

        Returns:
            List[str]: Logo as a list of strings, or empty list if size
                      is not available

        Raises:
            NotImplementedError: Must be implemented by subclasses
        """
        pass

    @abstractmethod
    def get_available_sizes(self) -> List[int]:
        """Get list of available logo sizes.

        Returns:
            List[int]: Sorted list of available sizes
        """
        pass

    def select_best_logo(self, available_space: int) -> List[str]:
        """Select the best logo that fits in the available space.

        Args:
            available_space: Size of the available square space

        Returns:
            List[str]: The largest logo that fits, or smallest if none fit
        """
        sizes = self.get_available_sizes()
        if not sizes:
            return []

        # Find the largest logo that fits
        best_logo = None
        for size in sorted(sizes, reverse=True):
            if size <= available_space:
                best_logo = self.get_logo(size)
                break

        # If no logo fits, return the smallest
        if best_logo is None:
            best_logo = self.get_logo(sizes[0])

        return best_logo
