from typing import List
import uuid

from fastapi.routing import APIRouter

from pepper.models.geofences import Geofence

router = APIRouter(prefix="/api/geofences", tags=["geofences"])


@router.get("", response_model=list[Geofence])
async def get_geofences(search: str | None = None, page: int = 1, limit: int = 1000):
    return {"message": "geofences"}


@router.get("/{id:path}", response_model=Geofence)
async def get_geofence_by_id(id: uuid.UUID):
    return {"id": id}
