from typing import Optional

from pydantic import BaseModel


class ResolverURL(BaseModel):
    base: str
    auth: str | None = None
    device: str | None = None
    position: str | None = None
    forward: str | None = None
