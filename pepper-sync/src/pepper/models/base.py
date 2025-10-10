from tortoise import fields, models
from uuid6 import uuid7


class BaseModel(models.Model):
    id = fields.UUIDField(primary_key=True, default=uuid7, index=True)

    class Meta:
        abstract = True
