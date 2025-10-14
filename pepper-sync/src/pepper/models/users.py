from enum import Enum
from typing import TYPE_CHECKING

from tortoise import fields
from tortoise.contrib.pydantic import (PydanticModel, pydantic_model_creator,  # pyright: ignore[reportUnknownVariableType]
                                       pydantic_queryset_creator)  # pyright: ignore[reportUnknownVariableType]

from pepper.models.auditable import AuditModel

from .base import BaseModel


class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"

class UserModel(BaseModel, AuditModel):
    full_name = fields.CharField(max_length=256)  # pyright: ignore[reportUnannotatedClassAttribute]
    email = fields.CharField(max_length=128)  # pyright: ignore[reportUnannotatedClassAttribute]
    role = fields.CharEnumField(UserRole, max_length=64, default=UserRole.USER)  # pyright: ignore[reportUnannotatedClassAttribute]
    phone = fields.CharField(max_length=15)  # pyright: ignore[reportUnannotatedClassAttribute]
    password_hash = fields.CharField(max_length=1024)  # pyright: ignore[reportUnannotatedClassAttribute]

    class Meta:  # pyright: ignore[reportIncompatibleVariableOverride]
        table = "users"  # pyright: ignore[reportUnannotatedClassAttribute]
    class PydanticMeta:
        exclude = ["password_hash", "created_at", "modified_at"]  # pyright: ignore[reportUnannotatedClassAttribute]


if TYPE_CHECKING:

    class User(UserModel, PydanticModel):  # type:ignore[misc]  # pyright: ignore[reportGeneralTypeIssues]
        pass

    class UserInput(UserModel, PydanticModel):  # type:ignore[misc]  # pyright: ignore[reportGeneralTypeIssues]
        pass

else:
    User = pydantic_model_creator(UserModel, name="User")
    UserInput = pydantic_model_creator(
        UserModel, name="UserInput", exclude_readonly=True
    )

UserList = pydantic_queryset_creator(UserModel)
