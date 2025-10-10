from typing import Literal, Optional

from pydantic import BaseModel


class ResolverAuth(BaseModel):
    type: Optional[Literal["form", "token", "basic"]] = None
    token_key: Optional[str] = "Authorization"
    token_type: Optional[Literal["bearer", "basic", "jwt", "refresh"]] = None
    token: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
