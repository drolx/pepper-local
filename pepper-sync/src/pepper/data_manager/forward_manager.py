import json
from pepper import cache_device, cache_position
from pepper.data_manager.device_manager import DeviceManager
from pepper.data_manager.position_manager import PositionManager
from pepper.types.forward import ForwardObject
from pepper.types.res_options import ResolverOption


class ForwardManager:
    option: ResolverOption
    device_manager: DeviceManager
    position_manager: PositionManager
    
    def __init__(self, device_manager: DeviceManager, position_manager: PositionManager) -> None:
        self.device_manager = device_manager
        self.option = device_manager.option
        self.position_manager = position_manager

    def process(self) -> list[ForwardObject]:
        items: list[ForwardObject] = []
        cached_devices = cache_device.get_all() #self.device_manager.get_by_resolver()
        cached_positions = cache_position.get_all() #self.position_manager.get_by_resolver()

        for device in cached_devices:
            if len(cached_positions) == 0:
                continue
            selected_position = next(
                (d for d in cached_positions if d['device_id'] == device["id"]),
                None  # This is the default value if no match is found
            )
            if selected_position is None:
                continue
                
            forward_object = {
                "id": device["id"],
                "name": device["name"],
                "time": device["time"],
                "unique_id": device["unique_id"],
                "status": device["status"],
                "speed": selected_position["speed"],
                "course": selected_position["course"],
                "altitude": selected_position["altitude"],
                "latitude": selected_position["lat"],
                "longitude": selected_position["lon"],
                "moved_at": None,
                "stoped_at": None,
                "address": "pending",
                "odometer": selected_position["odometer"] or 0,
                "battery": selected_position["battery"] or 0,
                "charging": selected_position["charging"] or True,
                "extras": {}
            }
            parsed_object = ForwardObject(**forward_object)
            items.append(parsed_object)

        print(items)
        return items
    
    def to_dict(self, payload: list[ForwardObject]) -> list[dict]:
        local_dict: list[dict] = []
        for obj in payload:
            json_str = obj.model_dump_json()
            local_dict.append(json.loads(json_str))
            
        return local_dict
    
