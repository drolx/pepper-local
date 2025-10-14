from abc import ABC, abstractmethod
import os
from typing import Literal

import httpx
from pepper import key_cache, logger, config
from pepper.converters.base import BaseConverter
from pepper.models.devices import DeviceInput
from pepper.models.positions import PositionInput
from pepper.types.forward import ForwardObject
from pepper.types.res_options import ResolverOption


class BaseResolver(ABC):
    option: ResolverOption
    converter: BaseConverter
    auth_key: str
    name: str
    base_url: str
    direction: str
    auth_token: str
    auth_type:  Literal["form", "token", "basic"]
    token_type: Literal["bearer", "basic", "jwt", "refresh"]
    token_key: str
    limit: int

    def __init__(self, option: ResolverOption):
        self.option = option
        self.name = option.name
        self.base_url = option.url.base
        self.direction = option.direction or "in"
        self.limit = config.options.max_items or 1000
        self.auth_key = f"auth:{self.__class__.__name__}"

        if option.auth is not None:
            self.auth_type = option.auth.type or "token"
            self.token_type = option.auth.token_type or "bearer"
            self.token_key = option.auth.token_key or "Authorization"
        
        if self.base_url == None:
            raise TypeError('Resolver base URL is missing...')
        
        local_token = self.get_local_token()
        if local_token is not None:
            self.auth_token = local_token
    
    def __endpont_url(self, path: str):
        is_base = path.lower().startswith("http")
        if is_base:
            return path
        else:
            return f"{self.base_url}{path}"

    def process(self) -> None:
        match self.direction:
            case "in":
                self.process_input()
            case "out":
                self.process_output()
            case _:
                logger.error("Unknown resolver requested")

    def get_auth_user(self):
        if self.option.auth is None:
            return None
        elif self.option.auth.username is not None and self.option.auth.username.startswith("$"):
            key = self.option.auth.username
            return os.getenv(key.lstrip("$"), "user")
        else:
            return self.option.auth.username

    def get_auth_pass(self):
        if self.option.auth is None:
            return None
        elif self.option.auth.password is not None and self.option.auth.password.startswith("$"):
            key = self.option.auth.password
            return os.getenv(key.lstrip("$"), "password")
        else:
            return self.option.auth.password

    def get_local_token(self):
        if self.option.auth is None:
            return None
        elif self.option.auth.token is not None and self.option.auth.token.startswith("$"):
            key = self.option.auth.token
            return os.getenv(key.lstrip("$"), "msssing_token")
        else:
            return self.option.auth.token

    def get_token(self) -> str:
        token = key_cache.get(self.auth_key)
        return str(token)

    def set_token(self, value: str):
        key_cache.set(self.auth_key, value)
        self.auth_token = self.get_token()

    def refresh_auth(self):
        pass

    def process_input(self):
        pass
    
    def process_output(self):
        pass

    @abstractmethod
    def resolve_auth(self):
        pass

    @abstractmethod
    def resolve_devices(self) -> httpx.Response:
        pass

    @abstractmethod
    def resolve_positions(self) -> httpx.Response:
        pass

    @abstractmethod
    def forward_positions(self, payload: list[ForwardObject]):
        pass