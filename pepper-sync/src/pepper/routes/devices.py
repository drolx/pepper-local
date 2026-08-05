import uuid

from typing import List
from fastapi.routing import APIRouter
from pepper.models import Device
from pepper import cache_device

router = APIRouter(prefix="/api/devices", tags=["devices"])


@router.get("", response_model=list)
async def get_devices(search: str | None = None, page: int = 1, limit: int = 1000):
    return cache_device.get_all()


@router.get("/{id:path}", response_model=Device)
async def get_device_by_id(id: uuid.UUID):
    return Device(id=id)
