from typing import override

import httpx
from pepper.types.forward import ForwardObject
from pepper.types.res_options import ResolverOption
from .base import BaseResolver


class WoxResolver(BaseResolver):
    def __init__(self, option: ResolverOption):
        super().__init__(option)

        if option.direction != "in":
            raise ValueError("Wrong resolver direction")

    @override
    def resolve_auth(self):
        url = self.__endpont_url(self.option.url.position  or "/api/login")
        with httpx.Client(base_url=url) as client:
            res = client.post("",
            headers = {
                    "Accept": "application/json",
            },
            data = {
                'email': self.get_auth_user(),
                'password': self.get_auth_pass(),
            })
            res_json = res.json()
            auth_value = res_json["user_api_hash"]
            self.set_token(auth_value)

    @override
    def resolve_devices(self) -> httpx.Response:
        url = self.__endpont_url(self.option.url.device  or "/api/get_devices")
        res: httpx.Response;
        with httpx.Client(base_url=url) as client:
            res = client.get("", headers={
                "Accept": "application/json",
            },
            params={
                "lang": "en",
                "limit": self.limit,
                "user_api_hash": self.get_token() 
            })
            
        return res


    @override
    def resolve_positions(self) -> httpx.Response:
        return self.resolve_devices()

    @override
    def forward_positions(self, payload: list[ForwardObject]):
        pass