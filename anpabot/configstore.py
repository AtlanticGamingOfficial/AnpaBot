
import discord
from peewee import SqliteDatabase, Model, IntegerField, CharField


class ConfigStore:

    def init_guild(self, guild: discord.Guild):
        db.connect()
        db.create_tables([BotAdminRole])

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



db = SqliteDatabase(f'botadmins.db')

class BaseModel(Model):
    class Meta:
        database = db

class BotAdminRole(BaseModel):
    guild_id = IntegerField(unique=False)
    role = CharField(unique=False)
