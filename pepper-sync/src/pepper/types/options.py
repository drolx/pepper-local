from typing import Annotated

from annotated_types import Gt
from pydantic import BaseModel

from .geocode_option import GeocodeOption


class ServerOption(BaseModel):
    version: float | None = 0.1
    title: str | None = "pepper.local"
    log_level: str | None = "INFO"
    log_db: bool | None = False
    host: str | None = "0.0.0.0"
    port: int | None = 8087
    refresh_interval: Annotated[int, Gt(4)] | None = 60
    request_timeout: Annotated[int, Gt(5)] | None = 10
    offline_interval: Annotated[int, Gt(60)] | None = 300
    auth_interval: Annotated[int, Gt(30)] | None = 3600
    max_items: Annotated[int, Gt(0)] | None = 1000
    database: str | None = "sqlite:///database.db"
    geocode: GeocodeOption | None = GeocodeOption()
    resolvers: list[str] | None = []
