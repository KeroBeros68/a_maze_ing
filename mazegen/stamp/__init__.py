"""Logo stamping module for maze generation.

Provides the Stamp class for embedding logos and artistic elements
into generated mazes. Supports multiple stamp designs through the
StampFactory pattern for extensibility.

Classes:
    Stamp: Manages stamp placement and embedding
    StampFactory: Factory for creating stamp designs
    StampDesign: Abstract base class for stamp designs
"""

from mazegen.stamp.Stamp import Stamp
from mazegen.stamp.stamp_factory import StampFactory
from mazegen.stamp.stamp_design import StampDesign


__all__ = ["Stamp", "StampFactory", "StampDesign"]
