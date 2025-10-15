from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

from pepper import logger
from pepper.cache.key_cache import KeyCache


InputType = TypeVar("InputType")
OutputType = TypeVar("OutputType")


class BaseHandler(ABC, Generic[InputType, OutputType]):
    cache: KeyCache

    def __init__(self, cache: KeyCache) -> None:
        super().__init__()
        self.cache = cache

    @abstractmethod
    async def process(self, input_data: InputType) -> OutputType:
        pass

    def get_cache(self, device_id: str) -> dict[str, Any] | None:
        pass
        # TODO: Change caching to dictionary based cache
        # return self.cache.get(f"device-{unique_id}", dict[str, Any]) # pyright: ignore[reportReturnType]

    def mutate_cache(self, device: dict[str, Any]):
        pass
        # TODO: adjustments to cache function
        # self.cache.set(
        #     f'device-{device["unique_id"]}',
        #     {
        #         "id": device["id"],
        #         "unique_id": device["unique_id"],
        #         "time": device["time"],
        #         "moved_at": device["moved_at"],
        #         "stoped_at": device["stoped_at"],
        #     },
        # )
        logger.info(f'Cached device: {device["unique_id"]} state successfully ...')

