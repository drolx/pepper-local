from typing import Annotated, Literal

from annotated_types import Gt
from pydantic import BaseModel

from .res_auth import ResolverAuth
from .res_url import ResolverEndpoint


class ResolverOption(BaseModel):
    name: str
    enable: bool | None = False
    persist: bool | None = False
    type: str
    address: str
    direction: Literal["in", "out"] = "in"
    interval: str | None = "*/5 * * * *"
    timeout: Annotated[int, Gt(0)] = 10
    auth: ResolverAuth | None = None
    headers: dict[str, str] | None = {}
    endpoints: ResolverEndpoint = ResolverEndpoint()

