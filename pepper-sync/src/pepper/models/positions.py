from typing import TYPE_CHECKING

from tortoise import fields
from tortoise.contrib.pydantic import (pydantic_model_creator,
                                       pydantic_queryset_creator)
from uuid6 import uuid7

from .base import BaseModel


class PositionModel(BaseModel):
    valid = fields.BooleanField()
    tag = fields.CharField(max_length=64)
    device_id = fields.UUIDField(default=uuid7, index=True)
    time = fields.DatetimeField(null=False)
    fix_time = fields.DatetimeField(null=False)
    speed = fields.FloatField(null=False)
    lat = fields.FloatField(null=False)
    lon = fields.FloatField(null=False)
    course = fields.FloatField(null=False)
    altitude = fields.FloatField(null=False)
    address = fields.CharField(max_length=1024)
    attributes = fields.JSONField()

    class Meta:
        table = "positions"
        ordering = ["time"]


if TYPE_CHECKING:

    class Position(PositionModel, PydanticModel):  # type:ignore[misc]
        pass

    class PositionInput(PositionModel, PydanticModel):  # type:ignore[misc]
        pass

else:
    Position = pydantic_model_creator(PositionModel, name="Position")
    PositionInput = pydantic_model_creator(
        PositionModel, name="PositionInput", exclude_readonly=True
    )

PositionList = pydantic_queryset_creator(PositionModel)
