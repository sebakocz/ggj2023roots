from tortoise import Model, fields


class Node(Model):
    """Node model."""

    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=30)
    parent_id = fields.IntField(null=True)
    channel_id = fields.BigIntField(null=True)
    role_id = fields.BigIntField(null=True)
    content = fields.JSONField(default={})