from abc import ABC, abstractmethod

from pepper.models.devices import Device
from pepper.models.geofences import Geofence
from pepper.models.positions import Position


class BaseConverter(ABC):
    devices: list[Device] = []

    @abstractmethod
    def resolve_devices(self, payload: dict[str, object]) -> None | list[Device]:
        pass

    @abstractmethod
    def resolve_positions(self, payload: dict[str, object]) -> None | list[Position]:
        pass

    @abstractmethod
    def resolve_geofences(self, payload: dict[str, object]) -> None | list[Geofence]:
        pass
