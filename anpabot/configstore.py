
import discord
from peewee import PostgresqlDatabase, Model, BigIntegerField, CharField
from playhouse.db_url import connect

class ConfigStore:
    def __init__(self, database_url: str):
        # self._database_url=database_url
        self.db = connect(database_url)
        self.db.bind([BotAdminRole, DefaultRole, MemberRole])
        self.db.connect()
        self.db.create_tables([BotAdminRole, DefaultRole, MemberRole])

    def _get_role_by_name(self, guild: discord.Guild, rolename):
        for guild_role in guild.roles:
            if guild_role.name == rolename:
                return guild_role
        return None

    def _get_role_by_id(self, guild: discord.Guild, roleid):
        for guild_role in guild.roles:
            if guild_role.id == roleid:
                return guild_role
        return None

    def is_admin(self, member: discord.Member):
        # Check for roles enabled to control the bot
        roles = list(BotAdminRole
            .select(BotAdminRole.role_id)
            .where(BotAdminRole.guild_id == member.guild.id))
        for admin_role_id in roles:
            if any(user_role.id == admin_role_id for user_role in member.roles):
                print(f'User has bot admin role')
                return True

        # Check for administrator permissions
        for role in member.roles:
            if role.permissions.administrator:
                print(f'User has guild admin role')
                return True

        # Owner should always be able to admin the bot
        return member.id == member.guild.owner_id

    def add_admin(self, guild: discord.Guild, rolename):
        role = self._get_role_by_name(guild, rolename)
        if role == None:
            print(f'Role {rolename} doesn\'t exists in guild {guild.name}#{guild.id}')
            return f'Role {rolename} doesn\'t exists in guild {guild.name}'
        roles = (BotAdminRole
            .select()
            .where(BotAdminRole.guild_id == guild.id, BotAdminRole.role_id == role.id))
        if (any(roles) == False):
            BotAdminRole.create(guild_id=guild.id, role_id=role.id, role_name=role.name)
            print(f'Adding role {role} to guild {guild.id}')
            return f'Added role {rolename} as bot admin'
        else:
            print(f'Role {role} already exists in guild {guild.name}#{guild.id}')
            return f'Role {rolename} already exists in guild {guild.name}'

    def set_default_role(self, guild: discord.Guild, rolename):
        role = self._get_role_by_name(guild, rolename)
        if role == None:
            print(f'Role {rolename} doesn\'t exists in guild {guild.name}#{guild.id}')
            return f'Role {rolename} doesn\'t exists in guild {guild.name}'
        roles = (DefaultRole
            .select()
            .where(DefaultRole.guild_id == guild.id, DefaultRole.role_id == role.id))
        if (any(roles) == False):
            DefaultRole.create(guild_id=guild.id, role_id=role.id, role_name=role.name)
            print(f'Setting default role {role} for guild {guild.name}#{guild.id}')
            return f'Setting default role {rolename} for guild {guild.name}'
        else:
            if (len(roles) > 1):
                print(f'Too many default roles for guild {guild.name}#{guild.id}')
                return f'Too many default roles for guild {guild.name}'
            role[0].role_id = role.id
            role[0].role_name = role.name
            role[0].save()
            print(f'Setting default role {role} for guild {guild.name}#{guild.id}')
            return f'Setting default role {rolename} for guild {guild.name}'

    def get_default_role(self, guild: discord.Guild):
        roles = list(DefaultRole
            .select()
            .where(DefaultRole.guild_id == guild.id))
        if (any(roles) == False):
            return None
        else:
            role = self._get_role_by_id(guild, roles[0].role_id)
            return role

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
