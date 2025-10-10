from typing import Optional

from pydantic import BaseModel


class ResolverURL(BaseModel):
    base: str
    auth: Optional[str] = None
    device: Optional[str] = None
    position: Optional[str] = None
