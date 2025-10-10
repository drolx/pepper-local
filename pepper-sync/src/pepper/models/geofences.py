from typing import TYPE_CHECKING

from tortoise import fields
from tortoise.contrib.pydantic import (pydantic_model_creator,
                                       pydantic_queryset_creator)

from .auditable import AuditModel
from .base import BaseModel


class GeofenceModel(BaseModel, AuditModel):
    name = fields.CharField(max_length=128, null=False)
    details = fields.CharField(max_length=1924, null=True)
    geometry = fields.JSONField()

    class Meta:
        table = "geofences"
        ordering = ["name"]


if TYPE_CHECKING:

    class Geofence(GeofenceModel, PydanticModel):  # type:ignore[misc]
        pass

    class GeofenceInput(GeofenceModel, PydanticModel):  # type:ignore[misc]
        pass

else:
    Geofence = pydantic_model_creator(GeofenceModel, name="Geofence")
    GeofenceInput = pydantic_model_creator(
        GeofenceModel, name="GeofenceInput", exclude_readonly=True
    )
GeofenceList = pydantic_queryset_creator(GeofenceModel)
