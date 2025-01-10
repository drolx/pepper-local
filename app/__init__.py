# Copyright (c) 2025 <Godwin peter. O>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
#  Project: thalia
#  Author: Godwin peter. O (me@godwin.dev)
#  Created At: Mon 06 Jan 2025 19:13:44
#  Modified By: Godwin peter. O (me@godwin.dev)
#  Modified At: Mon 06 Jan 2025 19:13:44

import asyncio
import json
import aiohttp
import logging
import os
import sys
from abc import ABC, abstractmethod
from datetime import datetime, time
from dbm import open
from typing import Any, Dict, Generic, List, Type, TypeVar, cast

from settings import GEOCODE_URL
from utils import CustomJSONEncoder

T = TypeVar("T", bool, str, int, float, complex, object, dict, list, tuple)

global_event_loop = asyncio.new_event_loop()

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)
logging.getLogger("sqlalchemy").setLevel(logging.ERROR)
logging.getLogger("sqlalchemy.pool").setLevel(logging.ERROR)
logging.getLogger("sqlalchemy.engine.Engine.app").setLevel(logging.ERROR)
app_logger = logging.getLogger(__name__)

today = datetime.today()
start_of_day = datetime.combine(today, time.min)
end_of_day = datetime.combine(today, time.max)


def parse_date_time(date_string: str, format: str = "%d-%m-%Y %H:%M:%S") -> datetime:
    parsed_datetime = datetime.strptime(date_string, format)

    return parsed_datetime


def get_process_path(requested_path: str = ""):
    exec_path = os.path.dirname(sys.argv[0])
    path = os.path.abspath(os.path.join(exec_path, requested_path))

    return path


class Cached:
    def __init__(self, location: str = "app"):
        path = get_process_path(".cache")
        os.makedirs(path, exist_ok=True)

        cache_path = os.path.join(path, location)
        self.instance = open(cache_path, "c")

    def get(self, key: str, get_type: Type[T] = object) -> T | None:
        byte_value = self.instance.get(key)

        if byte_value is None:
            return None

        value = str(byte_value, encoding="utf-8")
        _converted = json.loads(value)

        return cast(T, _converted)

    def set(self, key: str, value: object) -> object | None:
        _value = json.dumps(value, cls=CustomJSONEncoder)
        self.instance[key] = _value

    def clear(self) -> None:
        self.instance.clear()

    def close(self) -> None:
        self.instance.close()

    def __del__(self) -> None:
        self.close()


InputType = TypeVar("InputType")
OutputType = TypeVar("OutputType")


class Step(ABC, Generic[InputType, OutputType]):
    cache: Cached

    def __init__(self) -> None:
        super().__init__()
        self.cache = Cached()

    @abstractmethod
    async def process(self, input_data: InputType) -> OutputType:
        pass

    def get_device_cache(self, unique_id: str) -> Dict[str, Any] | None:
        # app_logger.info(f"Requested Cached device: {unique_id}...")
        return self.cache.get(f"device-{unique_id}", Dict[str, Any])

    def update_device_cache(self, device: Dict[str, Any]):
        self.cache.set(
            f"device-{device["unique_id"]}",
            {
                "id": device["id"],
                "unique_id": device["unique_id"],
                "time": device["time"],
                "moved_at": device["moved_at"],
                "stoped_at": device["stoped_at"],
            },
        )
        app_logger.info(f"Cached device: {device["unique_id"]} state successfully ...")


class Pipeline:
    def __init__(self) -> None:
        self.steps: List[Step[Any, Any]] = []

    def add_step(self, step: Step[InputType, OutputType]) -> None:
        if self.steps:
            # Validate type compatibility between last step's output and new step's input
            last_step = self.steps[-1]
            if not isinstance(last_step, Step) or not isinstance(step, Step):
                raise TypeError("Pipeline steps must inherit from the Step class.")

        self.steps.append(step)

    async def run(self, input_data: Any) -> Any:
        data: Any | None = input_data
        for step in self.steps:
            if data is None:
                break
            data = await step.process(data)

        await asyncio.sleep(2)

        return data


async def fetch_location_address(lat, lon) -> str | None:
    async with aiohttp.ClientSession() as session:
        url = f"{GEOCODE_URL}/reverse?format=geojson&lat={lat}&lon={lon}&addressdetails=0&zoom=18"
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.read()
                result = json.loads(data.decode("utf-8"))

                return result["features"][0]["properties"]["display_name"]
            else:
                app_logger.error(f"Error: {response.status}")
                return None
