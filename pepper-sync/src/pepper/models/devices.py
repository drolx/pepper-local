from enum import Enum
from typing import TYPE_CHECKING 

from tortoise import fields
from tortoise.contrib.pydantic import (PydanticModel, pydantic_model_creator,  # pyright: ignore[reportUnknownVariableType]
                                       pydantic_queryset_creator)  # pyright: ignore[reportUnknownVariableType]
from uuid6 import uuid7

from .auditable import AuditModel
from .base import BaseModel


class DeviceStatus(str, Enum):
    UNKNOWN = "unknown"
    OFFLINE = "offline"
    MOVING = "moving"
    PARKED = "parked"
    IDLING = "idling"

class DeviceModel(BaseModel, AuditModel):
    position_id = fields.UUIDField(default=uuid7, index=True)  # pyright: ignore[reportUnannotatedClassAttribute]
    resolver = fields.CharField(max_length=128, null=False)  # pyright: ignore[reportUnannotatedClassAttribute]
    name = fields.CharField(max_length=64, null=False)  # pyright: ignore[reportUnannotatedClassAttribute]
    time = fields.DatetimeField(null=True)  # pyright: ignore[reportUnannotatedClassAttribute]
    unique_id = fields.CharField(max_length=64, null=False, unique=True)  # pyright: ignore[reportUnannotatedClassAttribute]
    status = fields.CharEnumField(DeviceStatus, max_length=64)  # pyright: ignore[reportUnannotatedClassAttribute]
    odometer = fields.FloatField(null=True)  # pyright: ignore[reportUnannotatedClassAttribute]
    moved_at = fields.DatetimeField(null=True)  # pyright: ignore[reportUnannotatedClassAttribute]
    stoped_at = fields.DatetimeField(null=True)  # pyright: ignore[reportUnannotatedClassAttribute]
    battery = fields.FloatField(null=True)  # pyright: ignore[reportUnannotatedClassAttribute]
    charging = fields.BooleanField(default=False)  # pyright: ignore[reportUnannotatedClassAttribute]

    class Meta:  # pyright: ignore[reportIncompatibleVariableOverride]
        table = "devices"  # pyright: ignore[reportUnannotatedClassAttribute]
        ordering = ["name"]  # pyright: ignore[reportUnannotatedClassAttribute]


if TYPE_CHECKING:

    class Device(DeviceModel, PydanticModel):  # type:ignore[misc]  # pyright: ignore[reportGeneralTypeIssues]
        pass

    class DeviceInput(DeviceModel, PydanticModel):  # type:ignore[misc]  # pyright: ignore[reportGeneralTypeIssues]
        pass

else:
    Device = pydantic_model_creator(DeviceModel, name="Device")
    DeviceInput = pydantic_model_creator(
        DeviceModel, name="DeviceInput", exclude_readonly=True
    )
DeviceList = pydantic_queryset_creator(DeviceModel)
