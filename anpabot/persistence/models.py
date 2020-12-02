from peewee import Model, BigIntegerField, CharField


class RoleBaseModel(Model):
    guild_id = BigIntegerField(unique=False)
    role_id = BigIntegerField(unique=False)
    role_name = CharField(unique=False)


class BotAdminRole(RoleBaseModel):
    pass


class DefaultRole(RoleBaseModel):
    pass


class MemberRole(RoleBaseModel):
    pass
