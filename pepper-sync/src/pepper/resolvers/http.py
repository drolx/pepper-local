from typing import override

import httpx
from .base import BaseResolver


class HttpResolver(BaseResolver):
    @override
    async def resolve_auth(self):
        url = self.get_url_login("/api/session")
        pass

    @override
    async def resolve_devices(self) -> httpx.Response: # type: ignore
        url = self.get_url_device("/api/devices")
        res: httpx.Response;
        pass

    @override
    async def resolve_positions(self) -> httpx.Response: # type: ignore
        url = self.get_url_position("/api/positions")
        res: httpx.Response;
        pass

    @override
    async def forward_positions(self, payload: list[dict]):
        url = self.get_url_position("/api/positions")
        pass
