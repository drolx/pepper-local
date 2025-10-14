from typing import override

import httpx
from pepper.types.forward import ForwardObject
from .base import BaseResolver


class TraccarResolver(BaseResolver):
    @override
    def resolve_auth(self):
        url = self.__endpont_url(self.option.url.position  or "/api/session")
        pass

    @override
    def resolve_devices(self) -> httpx.Response: # type: ignore
        url = self.__endpont_url(self.option.url.position  or "/api/devices")
        res: httpx.Response;
        pass

    @override
    def resolve_positions(self) -> httpx.Response: # type: ignore
        url = self.__endpont_url(self.option.url.position  or "/api/positions")
        res: httpx.Response;
        pass

    @override
    def forward_positions(self, payload: list[ForwardObject]):
        pass