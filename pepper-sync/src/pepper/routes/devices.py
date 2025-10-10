import uuid

from typing import List
from fastapi.routing import APIRouter
from pepper.models import Device

router = APIRouter(prefix="/api/devices", tags=["devices"])


@router.get("", response_model=List[Device])
async def get_devices(search: str | None = None, page: int = 1, limit: int = 1000):
    return []


@router.get("/{id:path}", response_model=Device)
async def get_device_by_id(id: uuid.UUID):
    return Device(id=id)
