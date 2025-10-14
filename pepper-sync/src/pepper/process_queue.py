
import asyncio

# TODO: Implement periodic device cache
async def device_cache_queue():
    while True:
        print("======>>>  Refreshing devices cache...")
        await asyncio.sleep(10)

# TODO: Implement periodic position queue forwarding
async def position_storage_queue():
    while True:
        print("======>>>  Persist pending position data...")
        await asyncio.sleep(5)