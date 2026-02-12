"""Factory for selecting and instantiating maze generation algorithms.

This module provides the AlgorithmFactory class which implements the
Factory design pattern to create algorithm instances based on
configuration, supporting the Open/Closed Principle.
"""

from mazegen.algorithms.algorithm import MazeAlgorithm


class AlgorithmFactory:
    """Factory for creating maze generation algorithm instances.

    This class provides a centralized way to instantiate algorithms
    based on their name, allowing new algorithms to be added by
    extending the registry without modifying existing code.

    Class Attributes:
        __algorithms: Dictionary mapping algorithm names to classes
    """

    __algorithms: dict[str, type[MazeAlgorithm]] = {}

    @classmethod
    def _init_algorithms(cls) -> None:
        """Lazy load algorithms to avoid circular imports."""
        if not cls.__algorithms:
            from mazegen.algorithms.backtracking import BacktrackingAlgorithm
            cls.__algorithms = {
                "backtracking": BacktrackingAlgorithm,
            }

    @classmethod
    def create(cls, algorithm_name: str) -> MazeAlgorithm:
        """Create an algorithm instance by name.

        Args:
            algorithm_name: Name of the algorithm to create
                           (case-insensitive)

        Returns:
            MazeAlgorithm: An instance of the requested algorithm

        Raises:
            ValueError: If algorithm name is not registered
        """
        cls._init_algorithms()
        algo_name_lower = algorithm_name.lower().strip()

        if algo_name_lower not in cls.__algorithms:
            available = ", ".join(cls.__algorithms.keys())
            raise ValueError(
                f"Algorithm '{algorithm_name}' not found. "
                f"Available algorithms: {available}"
            )

        algorithm_class = cls.__algorithms[algo_name_lower]
        return algorithm_class()

    @classmethod
    def register(cls, name: str,
                 algorithm_class: type["MazeAlgorithm"]) -> None:
        """Register a new algorithm in the factory.

        This allows external code to register custom algorithms
        without modifying the factory itself.

        Args:
            name: Name identifier for the algorithm
            algorithm_class: The algorithm class to register

        Raises:
            TypeError: If algorithm_class doesn't implement MazeAlgorithm
        """
        from mazegen.algorithms.algorithm import MazeAlgorithm

        if not issubclass(algorithm_class, MazeAlgorithm):
            raise TypeError(
                f"{algorithm_class.__name__} must inherit from MazeAlgorithm"
            )

        cls._init_algorithms()
        cls.__algorithms[name.lower()] = algorithm_class

    @classmethod
    def get_available_algorithms(cls) -> list[str]:
        """Get list of available algorithm names.

        Returns:
            list[str]: Names of all registered algorithms
        """
        cls._init_algorithms()
        return list(cls.__algorithms.keys())
