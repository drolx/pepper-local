from typing import override
from pepper.cache.cache_manager import CacheManager
from pepper.handlers.base_position import BasePositionHandler
from pepper.models.positions import PositionInput


class PositionDistanceHandler(BasePositionHandler[PositionInput, PositionInput | None]):
    def __init__(self, cache: CacheManager) -> None:
        super().__init__(cache)

    @override
    async def process(self, input_data: PositionInput) -> PositionInput | None:
        pass
