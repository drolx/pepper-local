from datetime import datetime
from typing import Any, cast, override

from pepper import logger
from pepper.models.devices import DeviceInput, DeviceStatus
from pepper.models.geofences import GeofenceInput
from pepper.models.positions import PositionInput
from pepper.utils import parse_date_time

from .base import BaseConverter, PayloadObject


class WoxConverter(BaseConverter):
    def __process_dict(self, payload: PayloadObject) -> list[dict[str, Any]]:
        flat_items: list[dict[str, Any]] = []
        casted_payload: Any = payload
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
        payload_items = self.__process_dict(payload)
        results: list[DeviceInput] = []
        for obj in payload_items:
            dsert = DeviceInput(
                name = obj["name"],
                time = parse_date_time(obj["time"]),
                unique_id = obj["device_data"]["imei"],
                status = DeviceStatus.OFFLINE,
                resolver = "test"
            )
            results.append(dsert)
            # position_id, resolver, odometer, moved_at
            # stopped_at, battery, charging

        return results

    @override
    def resolve_positions(self, payload: PayloadObject) -> list[PositionInput]:
        payload_items = self.__process_dict(payload)
        results: list[PositionInput] = []
        for obj in payload_items:
            dsert = PositionInput(
                speed = obj["speed"],
                lat = obj["lat"],
                lon = obj["lng"],
                course = obj["course"],
                time = parse_date_time(obj["time"]),
                resolver = "test",
                altitude = obj["altitude"],
                fix_time = datetime.now()
            )
            results.append(dsert)
            # resolver, valid, resolver, device_id, time
            # fix_time, speed, lat, lon, course
            # altitude, address, attributes
        return results

    @override
    def resolve_geofences(self, payload: PayloadObject) -> list[GeofenceInput]:
        return []


