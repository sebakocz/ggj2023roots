from tortoise import Model, fields


class Node(Model):
    """Node model."""

    name = fields.CharField(max_length=30)

