from typing import Annotated, List, Optional

from annotated_types import Gt
from pydantic import BaseModel

from .geocode_option import GeocodeOption


class ServerOption(BaseModel):
    version: Optional[float] = 0.1
    title: Optional[str] = "pepper.local"
    log_level: Optional[str] = "INFO"
    log_db: Optional[bool] = False
    host: Optional[str] = "0.0.0.0"
    port: Optional[int] = 8087
    refresh_interval: Optional[Annotated[int, Gt(4)]] = 60
    request_timeout: Optional[Annotated[int, Gt(5)]] = 10
    offline_interval: Optional[Annotated[int, Gt(60)]] = 300
    auth_interval: Optional[Annotated[int, Gt(30)]] = 3600
    max_items: Optional[Annotated[int, Gt(0)]] = 1000
    database: Optional[str] = "sqlite:///database.db"
    geocode: Optional[GeocodeOption] = GeocodeOption()
    resolvers: Optional[List[str]] = []
