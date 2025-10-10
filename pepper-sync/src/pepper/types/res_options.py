from typing import Annotated, Dict, Literal, Optional

from annotated_types import Gt
from pydantic import BaseModel

from .res_auth import ResolverAuth
from .res_url import ResolverURL


class ResolverOption(BaseModel):
    name: str
    persist: Optional[bool] = False
    type: str
    direction: Literal["in", "out"] = "in"
    interval: Annotated[int, Gt(4)] = 30
    timeout: Annotated[int, Gt(0)] = 10
    url: ResolverURL
    auth: Optional[ResolverAuth] = None
    headers: Optional[Dict[str, str]] = {}
