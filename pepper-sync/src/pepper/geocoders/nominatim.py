import json
from .base import BaseGeocoder


class NominatimGeocoder(BaseGeocoder):
    def get_address(self, lat: float, lon: float) -> str | None:
        # TODO: Implement resolution
        pass

    # async with aiohttp.ClientSession() as session:
    #     url = f"{GEOCODE_URL}/reverse?format=geojson&lat={lat}&lon={lon}&addressdetails=0&zoom=18"
    #     async with session.get(url) as response:
    #         if response.status == 200:
    #             data = await response.read()
    #             result = json.loads(data.decode("utf-8"))

    #             return result["features"][0]["properties"]["display_name"]
    #         else:
    #             app_logger.error(f"Error: {response.status}")
    #             return None

