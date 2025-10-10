import uuid
from datetime import datetime
from typing import Annotated, Dict, Literal

from annotated_types import Gt
from pydantic import BaseModel, PositiveFloat


class ForwardObject(BaseModel):
    id: uuid.UUID
    unique_id: str
    name: str
    time: datetime
    status: Literal["offline", "moving", "parked", "idling", "unknown"]
    speed: PositiveFloat
    latitude: Annotated[float, Gt(0)]
    longitude: Annotated[float, Gt(0)]
    course: PositiveFloat
    altitude: PositiveFloat
    moved_at: datetime
    stoped_at: datetime
    odometer: PositiveFloat
    battery: PositiveFloat
    charging: bool
    extras: Dict[str, str]
