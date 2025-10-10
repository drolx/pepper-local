from typing import TYPE_CHECKING

from tortoise import fields
from tortoise.contrib.pydantic import (pydantic_model_creator,
                                       pydantic_queryset_creator)

from pepper.models.auditable import AuditModel

from .base import BaseModel


class AddressModel(BaseModel, AuditModel):
    name = fields.CharField(max_length=1024)
    lat = fields.FloatField(null=False)
    lon = fields.FloatField(null=False)
    attributes = fields.JSONField()

    class Meta:
        table = "address"


if TYPE_CHECKING:

    class Address(AddressModel, PydanticModel):  # type:ignore[misc]
        pass

    class AddressInput(AddressModel, PydanticModel):  # type:ignore[misc]
        pass

else:
    Address = pydantic_model_creator(AddressModel, name="Address")
    AddressInput = pydantic_model_creator(
        AddressModel, name="AddressInput", exclude_readonly=True
    )

AddressList = pydantic_queryset_creator(AddressModel)
