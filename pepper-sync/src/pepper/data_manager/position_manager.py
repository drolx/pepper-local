import json
from typing import Any
from pepper import cache_device, cache_position, logger
from pepper.converters.base import BaseConverter
from pepper.data_manager.device_manager import DeviceManager
from pepper.models.positions import PositionInput
from pepper.types.res_options import ResolverOption
import uuid6


class PositionManager:
    resolver_type: str
    option: ResolverOption
    devices: DeviceManager
    converter: BaseConverter
    
    def __init__(self, device_manager: DeviceManager, converter: BaseConverter) -> None:
        self.devices = device_manager
        self.option = device_manager.option
        self.resolver_type = device_manager.option.type
        self.converter = converter

    def get_id(self, unique_id: str) -> str | None:
        results = cache_device.find(lambda d: d["unique_id"] == unique_id)
        if len(results) == 0:
            return None
        
        selected = results[0]
        
        return selected["id"]

    def get_by_resolver(self) -> list[dict[str, Any]]:
        results = cache_position.find(lambda d: d["resolver"] == self.option.name)
        return results
    
    def get(self, device_id: str) -> dict[str, Any] | None:
        results = cache_position.find(lambda d: d["device_id"] == device_id)
        if len(results) == 0:
            return None
        
        selected = results[0]
        
        return selected
    
    def upsert(self, payload: PositionInput):
        results = cache_position.find(lambda d: d["device_id"] == payload.device_id)
        if len(results) == 0:
            parsed_dict = json.loads(payload.model_dump_json())
            # TODO: Fix abitary uuid generation
            parsed_dict["id"] = uuid6.uuid7().__str__()
            cache_position.add(parsed_dict)
        else:
            def updater(d):
                payload_dict = json.loads(payload.model_dump_json())
                payload_dict["device_id"] = d["device_id"]
                return payload_dict
            cache_position.update(lambda x: x["device_id"] == payload.device_id, updater)
    
    def process(self, payload: Any):
        parsed = self.converter.resolve_positions(payload)
        for position_item in parsed:
            self.upsert(position_item)
        logger.info(f"""Processed {len(parsed)} new position""")
    
    def clear(self):
        cache_position.clear()
