from .base import BaseConverter
from .ihs import IhsConverter
from .traccar import TraccarConverter
from .wox import WoxConverter

__all__ = ["BaseConverter", "IhsConverter", "TraccarConverter", "WoxConverter"]

# Dynamically initialize resolver class using its name as a string
def create_converter_instance(class_name, *args, **kwargs):  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType, reportAny]
    """
    Dynamically create an instance of a class by its name.
    """
    if class_name in globals():
        return globals()[class_name](*args, **kwargs)  # pyright: ignore[reportAny]
    else:
        raise ValueError(f"Class '{class_name}' not found.")

