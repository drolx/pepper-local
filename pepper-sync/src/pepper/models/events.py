from enum import Enum
from typing import TYPE_CHECKING

from tortoise import fields
from tortoise.contrib.pydantic import (pydantic_model_creator,
                                       pydantic_queryset_creator)
from uuid6 import uuid7

from .base import BaseModel


class EventType(str, Enum):
    OVERSPEED = "overspeed"
    GEOFENCE_IN = "geofence_in"
    GEOFENCE_OUT = "geofence_out"
    POWER_LOSS = "power_loss"
    TAMPER = "tamper"


class EventModel(BaseModel):
    tag = fields.CharField(max_length=64)
    type = fields.CharEnumField(EventType, max_length=64)
    device_id = fields.UUIDField(default=uuid7, index=True)
    position_id = fields.UUIDField(default=uuid7, index=True)
    time = fields.DatetimeField(null=False)
    fix_time = fields.DatetimeField(null=False)
    attributes = fields.JSONField()

    class Meta:
        table = "events"
        ordering = ["time"]


if TYPE_CHECKING:

    class Event(EventModel, PydanticModel):  # type:ignore[misc]
        pass

    class EventInput(EventModel, PydanticModel):  # type:ignore[misc]
        pass

else:
    Event = pydantic_model_creator(EventModel, name="Event")
    EventInput = pydantic_model_creator(
        EventModel, name="EventInput", exclude_readonly=True
    )

EventList = pydantic_queryset_creator(EventModel)
