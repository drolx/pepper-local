from enum import Enum
from typing import TYPE_CHECKING

from tortoise import fields
from tortoise.contrib.pydantic import (pydantic_model_creator,
                                       pydantic_queryset_creator)

from .base import BaseModel


class EventType(str, Enum):
    OVERSPEED = "overspeed"


class ServerEventModel(BaseModel):
    tag = fields.CharField(max_length=64)
    type = fields.CharEnumField(EventType, max_length=64)
    time = fields.DatetimeField(null=False)
    attributes = fields.JSONField()

    class Meta:
        table = "server_events"
        ordering = ["time"]


if TYPE_CHECKING:

    class ServerEvent(ServerEventModel, PydanticModel):  # type:ignore[misc]
        pass

    class ServerEventInput(ServerEventModel, PydanticModel):  # type:ignore[misc]
        pass

else:
    ServerEvent = pydantic_model_creator(ServerEventModel, name="ServerEvent")
    ServerEventInput = pydantic_model_creator(
        ServerEventModel, name="ServerEventInput", exclude_readonly=True
    )

ServerEventList = pydantic_queryset_creator(ServerEventModel)
