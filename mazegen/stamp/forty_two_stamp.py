"""FortyTwo stamp design implementation.

This module provides the FortyTwo logo stamp design for 42 school branding.

Classes:
    FortyTwoStamp: 42 logo stamp design with all sizes
    FortyTwoVanillaStamp: 42 logo always in vanilla style
    FortyTwoCustomStamp: 42 logo with custom style (SMALL, MEDIUM, LARGE)
"""

from typing import List
from mazegen.stamp.stamp_design import StampDesign
from mazegen.stamp.StampConsts import FortyTwo


class FortyTwoVanillaStamp(StampDesign):
    """FortyTwo stamp design always in vanilla style.

    Returns the vanilla logo regardless of requested size.
    """

    def get_logo(self, size: int) -> List[str]:
        """Get a FortyTwo vanilla logo.

        Always returns the vanilla logo regardless of size.

        Args:
            size: Requested size of the logo (ignored)

        Returns:
            List[str]: Vanilla logo as a list of strings
        """
        return FortyTwo.VANILLA

    def get_available_sizes(self) -> List[int]:
        """Get available logo sizes.

        Returns:
            List[int]: List containing only vanilla size (9)
        """
        return [9]


class FortyTwoCustomStamp(StampDesign):
    """FortyTwo stamp design with custom style.

    Uses SMALL, MEDIUM, and LARGE sizes, excluding VANILLA.
    """

    def get_logo(self, size: int) -> List[str]:
        """Get a FortyTwo custom logo.

        Returns SMALL, MEDIUM, or LARGE based on requested size.

        Args:
            size: Requested size of the logo

        Returns:
            List[str]: Logo as a list of strings
        """
        # For custom, skip vanilla and use SMALL, MEDIUM, LARGE
        if size <= 1:
            return FortyTwo.SMALL
        elif size <= 17:
            return FortyTwo.MEDIUM
        else:
            return FortyTwo.LARGE

    def get_available_sizes(self) -> List[int]:
        """Get available logo sizes.

        Returns:
            List[int]: Sorted list of available sizes (1, 18)
        """
        return [1, 18]
