
import discord
from peewee import PostgresqlDatabase, Model, BigIntegerField, CharField
from playhouse.db_url import connect

class ConfigStore:
    def __init__(self, database_url: str):
        # self._database_url=database_url
        self.db = connect(database_url)
        self.db.bind([BotAdminRole])

    def init_guild(self, guild: discord.Guild):
        self.db.connect()
        self.db.create_tables([BotAdminRole])

    def is_admin(self, member: discord.Member):
        # Check for roles enabled to control the bot
        roles = list(BotAdminRole
            .select(BotAdminRole.role)
            .where(BotAdminRole.guild_id == member.guild.id))
        for admin_role in roles:
            if any(user_role.name == admin_role for user_role in member.roles):
                print(f'User has bot admin role')
                return True

        # Check for administrator permissions
        for role in member.roles:
            if role.permissions.administrator:
                print(f'User has guild admin role')
                return True

        # Owner should always be able to admin the bot
        return member.id == member.guild.owner_id

    def add_admin(self, guild: discord.Guild, role):
        roles = (BotAdminRole
            .select()
            .where(BotAdminRole.guild_id == guild.id, BotAdminRole.role == role))
        if (any(roles) == False):
            print(f'Adding role {role} to guild {guild.id}')
            BotAdminRole.create(guild_id=guild.id, role=role)
        else:
            print(f'Role {role} already exists in guild {guild.id}')

class BotAdminRole(Model):
    guild_id = BigIntegerField(unique=False)
    role = CharField(unique=False)
