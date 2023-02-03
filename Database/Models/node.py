from tortoise import Model, fields


class Node(Model):
    """Node model."""

    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=30)
    parent_id = fields.IntField(null=True)

