from pepper.cache.key_cache import KeyCache
from pepper.handlers.base import BaseHandler
from pepper.models.positions import PositionInput


class PositionDistanceHandler(BaseHandler[PositionInput, PositionInput | None]):
    def __init__(self, cache: KeyCache) -> None:
        super().__init__(cache)

    async def process(self, input_data: PositionInput) -> PositionInput | None:
        pass
