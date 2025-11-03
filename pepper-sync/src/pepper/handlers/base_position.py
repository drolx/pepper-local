from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar, override

from pepper.cache.cache_manager import CacheManager

from .base import BaseHandler
from pepper import logger


InputType = TypeVar("InputType")
OutputType = TypeVar("OutputType")


class BasePositionHandler(BaseHandler, Generic[InputType, OutputType]):
    cache: CacheManager

    def __init__(self, cache: CacheManager) -> None:
        super().__init__()
        self.cache = cache

    @abstractmethod
    @override
    async def process(self, input_data: InputType) -> OutputType:
        pass

    def get_cache(self, device_id: str) -> dict[str, Any] | None:
        pass

    def mutate_cache(self, device: dict[str, Any]):
        logger.info(f'Cached device: {device["unique_id"]} state successfully ...')
