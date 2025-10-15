from abc import ABC, abstractmethod
from typing import Any

from pepper.models.devices import DeviceInput
from pepper.models.geofences import GeofenceInput
from pepper.models.positions import PositionInput
from pepper.types.res_options import ResolverOption

PayloadList = list[dict[str, Any]]
PayloadObject = dict[str, Any] | PayloadList

class BaseConverter(ABC):
    devices: list[DeviceInput] = []
    resolver: ResolverOption
    
    def set_resolver(self, value: ResolverOption):
        self.resolver = value

    @abstractmethod
    def resolve_devices(self, payload: PayloadObject) -> list[DeviceInput]:
        pass

    @abstractmethod
    def resolve_positions(self, payload: PayloadObject) -> list[PositionInput]:
        pass

    @abstractmethod
    def resolve_geofences(self, payload: PayloadObject) -> list[GeofenceInput]:
        pass
