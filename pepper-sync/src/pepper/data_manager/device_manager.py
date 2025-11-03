import json
from typing import Any
from pepper import cache_device, cache_position
from pepper.models.devices import DeviceInput
from pepper.types.res_options import ResolverOption


class DeviceManager:
    resolver_type: str
    option: ResolverOption

    def __init__(self, option: ResolverOption):
        self.option = option
        self.resolver_type = option.type
    
    def get_id(self, unique_id: str) -> str | None:
        results = cache_device.find(lambda d: d["unique_id"] == unique_id)
        if len(results) == 0:
            return None
        selected = results[0]
        
        return selected["id"]
        
    def get(self, id: str):
        results = cache_device.find(lambda d: d["id"] == id)
        if len(results) == 0:
            return None
        return results[0]
    
    def get_all(self):
        results = cache_device.get_all()
        return results

    
    def add(self, payload: DeviceInput):
        cache_device.add(payload.model_dump())
    
    def upsert(self, payload: DeviceInput):
        results = cache_device.find(lambda d: d["id"] == payload.id)
        if len(results) == 0:
            parsed_dict = json.loads(payload.model_dump_json())
            cache_device.add(parsed_dict)
        else:
            def updater(d):
                payload_dict = json.loads(payload.model_dump_json())
                payload_dict["id"] = d["id"]
                return payload_dict
            cache_device.update(lambda x: x["id"] == payload.id, updater)
    
    def get_by_resolver(self) -> list[dict[str, Any]]:
        results = cache_device.find(lambda d: d["resolver"] == self.option.name)
        return results

    def replace(self, payload: list[DeviceInput]):
        cache_device.clear()
        cache_position.clear()
        parsed_dict: list[dict] = []
        for device in payload:
            obj = device.model_dump()
            parsed_dict.append(obj)
        
        cache_device.add_many(parsed_dict)
        
    def dict_replace(self, payload: list[dict]):
            cache_device.clear()
            cache_position.clear()
            cache_device.add_many(payload)

    
    def clear(self):
        cache_device.clear()