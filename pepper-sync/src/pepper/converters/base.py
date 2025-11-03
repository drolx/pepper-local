from abc import ABC, abstractmethod
from typing import Any, Final

from pepper.models.devices import DeviceInput
from pepper.models.geofences import GeofenceInput
from pepper.models.positions import PositionInput
from pepper.types.res_options import ResolverOption
from pepper import cache_device

PayloadList = list[dict[str, Any]]
PayloadObject = dict[str, Any] | PayloadList

# TODO: Refactor all converters to use field getter, dict processing, validation and object method should be refined
class BaseConverter(ABC):
    resolver: ResolverOption
    resolver_name: str
    
    def __init__(self, option: ResolverOption) -> None:
        RES_SUFFIX: Final = "Converter"
        res_name = self.__class__.__name__
        if res_name.endswith(RES_SUFFIX):
            res_class_name = res_name.removesuffix(RES_SUFFIX)
            self.resolver_name = res_class_name.lower()
        
        self.resolver = option
        self.resolver_name = option.name.replace(" ", "")
    
    @abstractmethod
    def resolve_devices(self, payload: PayloadObject) -> list[DeviceInput]:
        pass

    @abstractmethod
    def resolve_positions(self, payload: PayloadObject) -> list[PositionInput]:
        pass

    @abstractmethod
    def resolve_geofences(self, payload: PayloadObject) -> list[GeofenceInput]:
        pass

    def resolve_device_id(self, unique_id: str) -> str | None:
        results = cache_device.find(lambda d: d["unique_id"] == unique_id)
        if len(results) == 0:
            return None
    
        selected = results[0]
        
        return selected["id"]

    def validate_dict(self, required_fields: list[str], input_data: dict[str, Any]) -> dict[str, Any] | None:
        for field in required_fields:
            keys = field.split(".")
            value = input_data
            try:
                for key in keys:
                    value = value[key]
            except (KeyError, TypeError):
                return None
            if value is None:
                return None

        return input_data
