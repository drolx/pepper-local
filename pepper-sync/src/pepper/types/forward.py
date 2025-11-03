import uuid
from datetime import datetime
from typing import Annotated, Dict, Literal

from annotated_types import Gt
from pydantic import BaseModel, PositiveFloat


class ForwardObject(BaseModel):
    id: uuid.UUID | None
    unique_id: str
    name: str
    time: datetime
    status: Literal["offline", "moving", "parked", "idling", "unknown"] = 'unknown'
    speed: float | None = 0.0
    latitude: float | None = 0.0
    longitude: float | None = 0.0
    address: str | None = ""
    course: float | None
    altitude: float | None
    moved_at: datetime | None
    stoped_at: datetime | None
    odometer: float | None
    battery: float | None
    charging: bool = True
    extras: Dict[str, str] = {}
