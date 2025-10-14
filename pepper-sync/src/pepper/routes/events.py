import uuid

from fastapi.routing import APIRouter
from typing import List

from pepper.models import Event

router = APIRouter(prefix="/api/events", tags=["events"])


@router.get("", response_model=list[Event])
async def get_events(search: str | None = None, page: int = 1, limit: int = 1000):
    return {"message": "events"}


@router.get("/{id:path}", response_model=Event)
async def get_event_by_id(id: uuid.UUID):
    return {"id": id}
