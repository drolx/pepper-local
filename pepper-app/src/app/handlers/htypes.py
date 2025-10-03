from typing import Any, Dict, TypedDict

from app.models import Device, Position

DeviceInput = TypedDict(
    "DeviceInput", {"Device": Dict[str, Any], "Source": Dict[str, Any]}
)
PositionInput = TypedDict(
    "PositionInput", {"Device": Dict[str, Any], "Position": Dict[str, Any]}
)
