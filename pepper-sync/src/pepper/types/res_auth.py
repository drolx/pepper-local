from typing import Literal, Optional

from pydantic import BaseModel


class ResolverAuth(BaseModel):
    type: Literal["form", "token", "basic"] | None = None
    token_key: str | None = "Authorization"
    token_type: Literal["bearer", "basic", "jwt", "refresh"] = "bearer"
    token: str | None = None
    username: str | None = None
    password: str | None = None
    headers: dict[str, str] | None = {}
