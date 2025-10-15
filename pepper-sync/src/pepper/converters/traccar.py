from typing import Any, override

from pepper.models.devices import DeviceInput
from pepper.models.geofences import GeofenceInput
from pepper.models.positions import PositionInput
from .base import BaseConverter, PayloadObject


class TraccarConverter(BaseConverter):
    @override
    def resolve_devices(self, payload: PayloadObject) -> list[DeviceInput]:
        return []

    @override
    def resolve_positions(self, payload: PayloadObject) -> list[PositionInput]:
        return []

    @override
    def resolve_geofences(self, payload: PayloadObject) -> list[GeofenceInput]:
        return []

