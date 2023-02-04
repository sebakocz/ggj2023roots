from tortoise import Model, fields


class User(Model):
    """User model."""

    name = fields.CharField(max_length=30)
    discord_id = fields.BigIntField(unique=True)
    where = fields.ForeignKeyField("models.Node", related_name="users", null=True, default=None)