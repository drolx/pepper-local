from typing import List
import uuid
from pepper import cache_position

from fastapi.routing import APIRouter

from pepper.models.positions import Position

router = APIRouter(prefix="/api/positions", tags=["positions"])


@router.get("", response_model=list)
async def get_positions(search: str | None = None, page: int = 1, limit: int = 1000):
    return cache_position.get_all()
    # return {"message": "positions"}


@router.get("/{id:path}", response_model=Position)
async def get_position_by_id(id: uuid.UUID):
    return {"id": id}
