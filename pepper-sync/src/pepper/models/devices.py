from enum import Enum
from typing import TYPE_CHECKING

from tortoise import fields
from tortoise.contrib.pydantic import (pydantic_model_creator,
                                       pydantic_queryset_creator)
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
    position_id = fields.UUIDField(default=uuid7, index=True)
    name = fields.CharField(max_length=64, null=False)
    time = fields.DatetimeField(null=True)
    unique_id = fields.CharField(max_length=64, null=False)
    status = fields.CharEnumField(DeviceStatus, max_length=64)
    odometer = fields.FloatField(null=True)
    moved_at = fields.DatetimeField(null=True)
    stoped_at = fields.DatetimeField(null=True)
    battery = fields.FloatField(null=True)
    charging = fields.BooleanField(default=False)

    class Meta:
        table = "devices"
        ordering = ["name"]


if TYPE_CHECKING:

    class Device(DeviceModel, PydanticModel):  # type:ignore[misc]
        pass

    class DeviceInput(DeviceModel, PydanticModel):  # type:ignore[misc]
        pass

else:
    Device = pydantic_model_creator(DeviceModel, name="Device")
    DeviceInput = pydantic_model_creator(
        DeviceModel, name="DeviceInput", exclude_readonly=True
    )
DeviceList = pydantic_queryset_creator(DeviceModel)
