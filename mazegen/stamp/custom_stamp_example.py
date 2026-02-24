"""Example custom stamp design implementation.

This module demonstrates how to create and register a custom stamp design
that can be used with the Stamp class.

Classes:
    CustomStamp: Example custom stamp design implementation
"""

from typing import List
from mazegen.stamp.stamp_design import StampDesign


class CustomStamp(StampDesign):
    """Example custom stamp design.

    This is a template showing how to implement a custom stamp design
    for use with the StampFactory.
    """

    def get_logo(self, size: int) -> List[str]:
        """Get a custom logo for the given size.

        Args:
            size: Requested size of the logo

        Returns:
            List[str]: Logo as a list of strings
        """
        # Define your logos for different sizes
        tiny = ["X"]

        small = [
            "XXX",
            "X X",
            "XXX",
        ]

        large = [
            "XXXXX",
            "X   X",
            "X   X",
            "X   X",
            "XXXXX",
        ]

        if size <= 1:
            return tiny
        elif size <= 3:
            return small
        else:
            return large

    def get_available_sizes(self) -> List[int]:
        """Get available logo sizes.

        Returns:
            List[int]: Sorted list of available sizes (1, 3, 5)
        """
        return [1, 3, 5]


# To use this custom stamp, register it with the factory:
#
# from mazegen.stamp.stamp_factory import StampFactory
# from examples.custom_stamp import CustomStamp
#
# StampFactory.register("mycustom", CustomStamp)
#
# Then use it:
# stamp = Stamp(maze, "mycustom")
# stamp.add_stamp()
