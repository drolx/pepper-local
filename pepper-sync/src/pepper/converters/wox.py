from datetime import datetime
from typing import Any, cast, override

from pepper import logger
from pepper.models.devices import DeviceInput, DeviceStatus
from pepper.models.geofences import GeofenceInput
from pepper.models.positions import PositionInput
from pepper.types.res_options import ResolverOption
from pepper.utils import parse_date_time

from .base import BaseConverter, PayloadObject


class WoxConverter(BaseConverter):
    def __init__(self, option: ResolverOption) -> None:
        super().__init__(option)

    def __process_dict__(self, payload: PayloadObject) -> list[dict[str, Any]]:
        flat_items: list[dict[str, Any]] = []
        casted_payload: Any = payload
        
        if casted_payload is None:
            return []
        
        try:
            for grouped_item in casted_payload:
                grouped_obj = grouped_item["items"]
                if grouped_obj is not None:
                    flat_items.extend(grouped_obj)
        except Exception as e:
            logger.error(f"error parsing recieved payload", e)


        return flat_items

    @override
    def resolve_devices(self, payload: PayloadObject) -> list[DeviceInput]:
        payload_items = self.__process_dict__(payload)
        results: list[DeviceInput] = []
        for obj in payload_items:
            dsert = DeviceInput(
                name = obj["name"],
                time = parse_date_time(obj["time"]),
                unique_id = obj["device_data"]["imei"],
                status = DeviceStatus.OFFLINE,
                resolver = self.resolver_name
            )
            results.append(dsert)
            # position_id, resolver, odometer, moved_at
            # stopped_at, battery, charging

        return results

    @override
    def resolve_positions(self, payload: PayloadObject) -> list[PositionInput]:
        payload_items = self.__process_dict__(payload)
        results: list[PositionInput] = []
        required_fields = [
            "name",
            "time",
            "lat",
            "course",
            "speed",
            "altitude",
            "address",
            "protocol",
            "device_data.imei",
            "device_data.traccar.moved_at",
            "device_data.traccar.stoped_at",
            "device_data.traccar.protocol",
        ]

        for obj in payload_items:
            validation = self.validate_dict(required_fields, obj)
            unique_id: str = obj["device_data"]["imei"]
            device_id = self.resolve_device_id(unique_id)
            
            if validation is None or device_id is None:
                logger.error("Failed to complete position validation/processing")
                return []
            
            obj_dict = {
                # "id": uuid6.uuid7(),
                "device_id": device_id,
                "valid": True,
                "speed": obj["speed"],
                "lat": obj["lat"],
                "lon": obj["lng"],
                "course": obj["course"],
                "time": parse_date_time(obj["time"]),
                "resolver": self.resolver_name,
                "altitude": obj["altitude"],
                "fix_time": datetime.now()
            }
            dsert = PositionInput(**obj_dict)
            results.append(dsert)
            # valid, address, attributes
        return results

    @override
    def resolve_geofences(self, payload: PayloadObject) -> list[GeofenceInput]:
        return []


