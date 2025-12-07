from typing import override

import httpx
from pepper.types.res_options import ResolverOption
from .base import BaseResolver


class WoxResolver(BaseResolver):
    def __init__(self, option: ResolverOption):
        super().__init__(option)

        if option.direction != "in":
            raise ValueError("Wrong resolver direction")

    @override
    async def resolve_auth(self):
        url = self.get_url_login("/api/login")
        try:
            async with httpx.AsyncClient() as client:
                auth_data = {
                    "email": self.get_auth_user(),
                    "password": self.get_auth_pass(),
                }
                response = await client.post(
                    url,
                    headers={
                        "Accept": "application/json",
                    },
                    data=auth_data,
                )
                response.raise_for_status()
                res_json = response.json()
                auth_value = res_json["user_api_hash"] or ""
                self.set_token(auth_value)
        except httpx.HTTPError as e:
            self.logger.error("error completing auth request", e)

    @override
    async def resolve_devices(self) -> httpx.Response | None:
        await self.check_auth()
        url = self.get_url_device("/api/get_devices")
        token = self.get_token()
        response: httpx.Response
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    url,
                    timeout=300,
                    headers={
                        "Accept": "application/json",
                    },
                    params={"lang": "en", "limit": self.limit, "user_api_hash": token},
                )

                return await self.process_response(response, self.resolve_devices)

        except httpx.HTTPError as e:
            self.logger.error("error completing devices request", e)

    @override
    async def resolve_positions(self) -> httpx.Response | None:
        return await self.resolve_devices()

    @override
    async def forward_positions(self, payload: list[dict]):
        pass
