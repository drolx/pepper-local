from typing import List

from fastapi.routing import APIRouter

from pepper import config
from pepper.types.res_options import ResolverOption

router = APIRouter(prefix="/api/resolvers", tags=["resolvers"])


@router.get("", response_model=List[ResolverOption])
async def get_resolvers(search: str | None = None, page: int = 1, limit: int = 1000):
    res = config.resolvers
    return res
