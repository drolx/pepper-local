from typing import override

from pepper.models.devices import Device
from pepper.models.geofences import Geofence
from pepper.models.positions import Position
from .base import BaseConverter


class TraccarConverter(BaseConverter):
    @override
    def resolve_devices(self, payload: dict[str, object]) -> None | list[Device]:
        pass

    @override
    def resolve_positions(self, payload: dict[str, object]) -> None | list[Position]:
        pass

    @override
    def resolve_geofences(self, payload: dict[str, object]) -> None | list[Geofence]:
        pass

