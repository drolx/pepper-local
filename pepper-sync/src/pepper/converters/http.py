from typing import override

from pepper.models.devices import DeviceInput
from pepper.models.geofences import GeofenceInput
from pepper.models.positions import PositionInput
from pepper.types.res_options import ResolverOption
from .base import BaseConverter, PayloadObject


class HttpConverter(BaseConverter):
    def __init__(self, option: ResolverOption) -> None:
        super().__init__(option)
    
    @override
    def resolve_devices(self, payload: PayloadObject) -> list[DeviceInput]:
        return []

    @override
    def resolve_positions(self, payload: PayloadObject) -> list[PositionInput]:
        return []

    @override
    def resolve_geofences(self, payload: PayloadObject) -> list[GeofenceInput]:
        return []


