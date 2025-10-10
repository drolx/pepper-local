from fastapi.routing import APIRouter

from pepper import config
from pepper.models.service_events import ServerEvent
from pepper.types.options import ServerOption

router = APIRouter(prefix="/api/server", tags=["server"])


@router.get("", response_model=ServerOption)
async def get_server_options():
    res = config.options
    return res


@router.get("/events", response_model=ServerEvent)
async def get_server_events(
    search: str | None = None, page: int = 1, limit: int = 1000
):
    return ServerEvent()
