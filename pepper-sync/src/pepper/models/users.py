from enum import Enum
from typing import TYPE_CHECKING

from tortoise import fields
from tortoise.contrib.pydantic import (pydantic_model_creator,
                                       pydantic_queryset_creator)

from pepper.models.auditable import AuditModel

from .base import BaseModel


class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"

class UserModel(BaseModel, AuditModel):
    full_name = fields.CharField(max_length=256)
    email = fields.CharField(max_length=128)
    role = fields.CharEnumField(UserRole, max_length=64, default=UserRole.USER)
    phone = fields.CharField(max_length=15)
    password_hash = fields.CharField(max_length=1024)

    class Meta:
        table = "users"
    class PydanticMeta:
        exclude = ["password_hash", "created_at", "modified_at"]


if TYPE_CHECKING:

    class User(UserModel, PydanticModel):  # type:ignore[misc]
        pass

    class UserInput(UserModel, PydanticModel):  # type:ignore[misc]
        pass

else:
    User = pydantic_model_creator(UserModel, name="User")
    UserInput = pydantic_model_creator(
        UserModel, name="UserInput", exclude_readonly=True
    )

UserList = pydantic_queryset_creator(UserModel)
