from tortoise import fields, models


class AuditModel(models.Model):
    #: The date-time the Device record was created at
    created_at = fields.DatetimeField(auto_now_add=True)
    #: The date-time the Device record was modified at
    modified_at = fields.DatetimeField(auto_now=True)

    class Meta:
        abstract = True
