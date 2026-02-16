"""Factory for creating and managing maze visualization views.

This module implements the Factory design pattern to create view instances
based on requested view type names, supporting extensibility
and loose coupling.

Classes:
    ViewFactory: Factory for creating and managing View instances
"""

from view.View import View
from model import ConfigModel



class ViewFactory:
    """Factory for creating view instances.

    Implements the Factory design pattern to create view objects based on
    view type names. Supports lazy initialization and extensibility through
    the register method.

    Class Attributes:
        __view: Dictionary mapping view names to view classes
    """
    __view: dict[str, type[View]] = {}

    @classmethod
    def _init_view(cls) -> None:
        """Initialize the view registry with available views.

        Lazily loads view classes to avoid circular imports.
        Called automatically on first use.
        """
        if not cls.__view:
            from view.basic import BasicView
            from view.tty import TtyView
            cls.__view = {
                "basic": BasicView,
                "tty": TtyView
            }

    @classmethod
    def create(cls, view_name: str, config: ConfigModel) -> View:
        """Create a view instance by name.

        Args:
            view_name: Name of the view type to create

        Returns:
            View: An instance of the requested view

        Raises:
            ValueError: If view name is not registered
        """
        cls._init_view()
        view_name_lower = view_name.lower().strip()

        if view_name_lower not in cls.__view:
            available = ", ".join(cls.__view.keys())
            raise ValueError(
                f"view '{view_name}' not found. "
                f"Available view: {available}"
            )

        view_class = cls.__view[view_name_lower]
        return view_class(config)

    @classmethod
    def get_available_view(cls) -> list[str]:
        """Get list of available view names.

        Returns:
            list[str]: Names of all registered views
        """
        cls._init_view()
        return list(cls.__view.keys())
