from tortoise import Model, fields


class User(Model):
    """User model."""

    name = fields.CharField(max_length=30)
