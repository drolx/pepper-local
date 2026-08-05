from abc import ABC, abstractmethod
import asyncio
import os
from typing import Any, Awaitable, Callable, Final, Literal

import logging
import httpx
from pepper import key_cache, logger as app_logger, config
from pepper.converters import create_converter_instance
from pepper.converters.base import BaseConverter
from pepper.data_manager.device_manager import DeviceManager
from pepper.data_manager.forward_manager import ForwardManager
from pepper.data_manager.position_manager import PositionManager
from pepper.models.devices import DeviceInput
from pepper.types.res_options import ResolverOption


class BaseResolver(ABC):
    request_attempts: int = 0
    max_attempts: int = 3
    resolver_type: str
    option: ResolverOption
    converter: BaseConverter
    auth_key: str
    name: str
    base_url: str
    direction: str
    is_auth: bool = False
    auth_token: str | None = None
    auth_type: Literal["form", "token", "basic"]
    token_type: Literal["bearer", "basic", "jwt", "refresh"]
    token_key: str
    limit: int
    logger: logging.Logger
    forwader: ForwardManager
    device_manager: DeviceManager
    position_manager: PositionManager

    def __init__(self, option: ResolverOption):
        RES_SUFFIX: Final = "Resolver"
        res_name = self.__class__.__name__
        if res_name.endswith(RES_SUFFIX):
            res_class_name = res_name.removesuffix(RES_SUFFIX)
            self.resolver_type = res_class_name.lower()

        if self.resolver_type is not None:
            converter_instance_name = self.resolver_type.capitalize()
            self.converter = create_converter_instance(
                f"{converter_instance_name}Converter", option
            )

        self.logger = app_logger
        self.option = option
        self.name = option.name
        self.base_url = option.address
        self.direction = option.direction or "in"
        self.limit = config.options.max_items or 1000
        self.auth_key = f"auth:{option.name.replace(' ', '')}"
        self.device_manager = DeviceManager(option)
        self.position_manager = PositionManager(self.device_manager, self.converter)
        self.forwader = ForwardManager(self.device_manager, self.position_manager)

        if option.auth is not None:
            self.auth_type = option.auth.type or "token"
            self.token_type = option.auth.token_type or "bearer"
            self.token_key = option.auth.token_key or "Authorization"

        if self.base_url is None:
            raise TypeError("Resolver base URL is missing...")

        local_token = self.get_local_token()
        if local_token is not None:
            self.auth_token = local_token

    def __endpont_url__(self, path: str):
        is_base = path.lower().startswith("http")
        if is_base:
            return path
        else:
            return f"{self.base_url}{path}"

    async def process(self) -> None | Any:
        match self.direction:
            case "in":
                return await self.process_input()
            case "out":
                return await self.process_output()
            case _:
                self.logger.error("Unknown resolver requested")

        return None

    def get_auth_user(self):
        if self.option.auth is None:
            return None
        elif (
            self.option.auth.username is not None
            and self.option.auth.username.startswith("$")
        ):
            key = self.option.auth.username
            return os.getenv(key.lstrip("$"), "user")
        else:
            return self.option.auth.username

    def get_auth_pass(self):
        if self.option.auth is None:
            return None
        elif (
            self.option.auth.password is not None
            and self.option.auth.password.startswith("$")
        ):
            key = self.option.auth.password
            return os.getenv(key.lstrip("$"), "password")
        else:
            return self.option.auth.password

    def get_local_token(self):
        if self.option.auth is None:
            return None
        elif self.option.auth.token is not None and self.option.auth.token.startswith(
            "$"
        ):
            key = self.option.auth.token
            return os.getenv(key.lstrip("$"), "msssing_token")
        else:
            return self.option.auth.token

    def get_token(self) -> str:
        token = key_cache.get(self.auth_key) or ""
        self.auth_token = str(token)
        return self.auth_token

    def set_token(self, value: str):
        if len(value) > 0:
            key_cache.set(self.auth_key, value)
            self.auth_token = self.get_token()
            self.is_auth = True

    async def refresh_auth(self):
        self.is_auth = False
        await self.resolve_auth()

    async def check_auth(self):
        token = self.get_token()
        if self.is_auth is False:
            await self.refresh_auth()
        elif len(token) < 1:
            self.is_auth = False
            await self.refresh_auth()

    async def process_input(self):
        raw_payload = await self.get_raw_positions()
        self.position_manager.process(raw_payload)

    async def process_output(self):
        payload = self.forwader.process()
        parsed = self.forwader.to_dict(payload)
        await self.forward_positions(parsed)

    @abstractmethod
    async def resolve_auth(self):
        pass

    @abstractmethod
    async def resolve_devices(self) -> httpx.Response | None:
        pass

    @abstractmethod
    async def resolve_positions(self) -> httpx.Response | None:
        pass

    @abstractmethod
    async def forward_positions(self, payload: list[dict]):
        pass

    async def process_response(
        self,
        response: httpx.Response,
        request_func: Callable[[], Awaitable[httpx.Response | None]],
    ):
        if response.status_code == 401:
            self.request_attempts += 1
            if self.request_attempts > self.max_attempts:
                self.logger.error("resolver authentication seems to have an issue")
                return response

            await asyncio.sleep(2)
            self.logger.error("request failed re-attempting authentication")
            await self.refresh_auth()
            return await request_func()
        else:
            self.request_attempts = 0
            return response

    async def process_forward_response(
        self,
        response: httpx.Response,
        request_func: Callable[[list[dict]], Awaitable[httpx.Response | None]],
        payload: list[dict],
    ):
        if response.status_code == 401:
            self.request_attempts += 1
            if self.request_attempts > self.max_attempts:
                self.logger.error("resolver authentication seems to have an issue")
                return response

            await asyncio.sleep(2)
            self.logger.error("request failed re-attempting authentication")
            await self.refresh_auth()
            return await request_func(payload)
        else:
            self.request_attempts = 0
            return response

    async def get_raw_devices(self) -> Any:
        response = await self.resolve_devices()
        if response is None:
            return None

        return response.json()

    async def get_devices(self) -> list[DeviceInput]:
        val = await self.get_raw_devices()
        return self.converter.resolve_devices(val)

    async def get_raw_positions(self) -> Any:
        response = await self.resolve_devices()
        if response is None:
            return None

        return response.json()

    async def get_raw_geofences(self) -> Any:
        response = await self.resolve_devices()
        if response is None:
            return None

        return response.json()

    def get_url_login(self, path: str | None):
        url_path = getattr(self.option.endpoints.login, "path", None) or path
        if url_path is None:
            raise ValueError("Login endpoint path is empty")
        url = self.__endpont_url__(url_path or "")
        return url

    def get_url_device(self, path: str | None):
        url_path = getattr(self.option.endpoints.device, "path", None) or path
        if url_path is None:
            raise ValueError("Device endpoint path is empty")
        url = self.__endpont_url__(url_path or "")
        return url

    def get_url_position(self, path: str | None):
        url_path = getattr(self.option.endpoints.position, "path", None) or path
        if url_path is None:
            raise ValueError("Position endpoint path is empty")
        url = self.__endpont_url__(url_path or "")
        return url

    def get_url_geofence(self, path: str | None):
        url_path = getattr(self.option.endpoints.geofence, "path", None) or path
        if url_path is None:
            raise ValueError("Geofence endpoint path is empty")
        url = self.__endpont_url__(url_path or "")
        return url
