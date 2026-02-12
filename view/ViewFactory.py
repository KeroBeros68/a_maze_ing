from view.View import View


class ViewFactory:
    __view: dict[str, type[View]] = {}

    @classmethod
    def _init_view(cls) -> None:
        if not cls.__view:
            from view.basic import BasicView
            cls.__view = {
                "basic": BasicView
            }

    @classmethod
    def create(cls, view_name: str) -> View:
        cls._init_view()
        view_name_lower = view_name.lower().strip()

        if view_name_lower not in cls.__view:
            available = ", ".join(cls.__view.keys())
            raise ValueError(
                f"view '{view_name}' not found. "
                f"Available view: {available}"
            )

        view_class = cls.__view[view_name_lower]
        return view_class()

    @classmethod
    def get_available_view(cls) -> list[str]:
        cls._init_view()
        return list(cls.__view.keys())
