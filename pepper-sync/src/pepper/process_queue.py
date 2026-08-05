import asyncio
import json

from pepper.data_manager.device_manager import DeviceManager
from pepper.resolvers import load_resolvers
import uuid6


# TODO: Implement periodic device cache
async def device_cache_queue():
    while True:
        print("======>>>  Refreshing devices cache...")
        for res in load_resolvers():
            # TODO: correct placeholder type condition
            if (
                res.resover_type == "wox"
                and res.enable
                and res.resolver_direction == "in"
            ):
                instance = res.instance
                manager = DeviceManager(instance.option)
                devices: list[dict] = []
                response_devices = await instance.get_devices()
                for dv in response_devices:
                    device = json.loads(dv.model_dump_json())
                    # TODO: Fix arbitrary uuid generation
                    device["id"] = uuid6.uuid7().__str__()
                    devices.append(device)

                # TODO: Fix wrong cache storage
                manager.dict_replace(devices)

        await asyncio.sleep(600)


# TODO: Implement periodic position queue forwarding
async def position_storage_queue():
    while True:
        print("======>>>  Persist queued position data...")
        await asyncio.sleep(5)
