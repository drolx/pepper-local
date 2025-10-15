from typing import TYPE_CHECKING

from tortoise import fields
from tortoise.contrib.pydantic import (PydanticModel, pydantic_model_creator,  # pyright: ignore[reportUnknownVariableType]
                                       pydantic_queryset_creator)  # pyright: ignore[reportUnknownVariableType]
from uuid6 import uuid7

from .base import BaseModel


class PositionModel(BaseModel):
    resolver = fields.CharField(max_length=128, null=False)  # pyright: ignore[reportUnannotatedClassAttribute]
    valid = fields.BooleanField(default=True)  # pyright: ignore[reportUnannotatedClassAttribute]
    device_id = fields.UUIDField(default=uuid7, db_index=True, null=True)  # pyright: ignore[reportUnannotatedClassAttribute]
    time = fields.DatetimeField(null=False)  # pyright: ignore[reportUnannotatedClassAttribute]
    fix_time = fields.DatetimeField(null=False)  # pyright: ignore[reportUnannotatedClassAttribute]
    speed = fields.FloatField(null=False)  # pyright: ignore[reportUnannotatedClassAttribute]
    lat = fields.FloatField(null=False)  # pyright: ignore[reportUnannotatedClassAttribute]
    lon = fields.FloatField(null=False)  # pyright: ignore[reportUnannotatedClassAttribute]
    course = fields.FloatField(null=False)  # pyright: ignore[reportUnannotatedClassAttribute]
    altitude = fields.FloatField(null=False)  # pyright: ignore[reportUnannotatedClassAttribute]
    address = fields.CharField(max_length=1024, null=True)  # pyright: ignore[reportUnannotatedClassAttribute]
    attributes = fields.JSONField(default={})  # pyright: ignore[reportUnknownVariableType, reportUnannotatedClassAttribute]

    class Meta:  # pyright: ignore[reportIncompatibleVariableOverride]
        table = "positions"  # pyright: ignore[reportUnannotatedClassAttribute]
        ordering = ["time"]  # pyright: ignore[reportUnannotatedClassAttribute]


if TYPE_CHECKING:

    class Position(PositionModel, PydanticModel):  # type:ignore[misc]  # pyright: ignore[reportGeneralTypeIssues]
        pass

    class PositionInput(PositionModel, PydanticModel):  # type:ignore[misc]  # pyright: ignore[reportGeneralTypeIssues]
        pass

else:
    Position = pydantic_model_creator(PositionModel, name="Position")
    PositionInput = pydantic_model_creator(
        PositionModel, name="PositionInput", exclude_readonly=True
    )

PositionList = pydantic_queryset_creator(PositionModel)
