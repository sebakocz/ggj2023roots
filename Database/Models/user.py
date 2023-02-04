from tortoise import Model, fields


class User(Model):
    """User model."""

    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=30)
    discord_id = fields.BigIntField(unique=True)
    where = fields.ForeignKeyField("models.Node", related_name="users", null=True, default=None)
    score = fields.IntField(default=0)
    trojan_last_created_at = fields.IntField(null=True)
    virus_last_created_at = fields.IntField(null=True)
    worm_last_created_at = fields.IntField(null=True)
    anti_virus_last_created_at = fields.IntField(null=True)
    firewall_last_created_at = fields.IntField(null=True)
    patching_last_created_at = fields.IntField(null=True)