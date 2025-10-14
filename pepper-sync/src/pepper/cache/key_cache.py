
from dbm import open
import json
import os
from typing import TypeVar, cast

from pepper.utils import get_process_path

T = TypeVar("T", bool, str, int, float, complex, object, dict, list, tuple)

class KeyCache:
    def __init__(self, location: str = "app"):
        path = get_process_path(".cache")
        os.makedirs(path, exist_ok=True)

        cache_path = os.path.join(path, location)
        self.instance = open(cache_path, "c")

    def get(self, key: str, get_type: T | None = object) -> T | None:
        byte_value = self.instance.get(key)

        if byte_value is None:
            return None

        value = str(byte_value, encoding="utf-8")
        _converted = json.loads(value)

        return cast(T, _converted)

    def set(self, key: str, value: object) -> object | None:
        _value = json.dumps(value)
        self.instance[key] = _value

    def clear(self) -> None:
        for key in list(self.instance.keys()):
            del self.instance[key]
            # self.instance.clear()

    def close(self) -> None:
        self.instance.close()

    def __del__(self) -> None:
        self.close()